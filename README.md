# Decentralized Cloud-Based File Storage

A way to encrypt and upload files to multiple servers. **This project is still in development and not ready for deployment.**

This document outlines the structure and philosophy of the project. If you're interested in contributing, please read the [contributing guidelines](https://github.com/darcymeyer/dcbfs/blob/master/CONTRIBUTING.md) and [code of conduct](https://github.com/darcymeyer/dcbfs/blob/master/CODE_OF_CONDUCT.md).

### Installation

To install dcbfs to `/usr/local/bin/`, run the following line in a terminal: 
`python setup.py install --install-scripts=/usr/local/bin`

### How to use

dcbfs is used as a command line tool.

	Usage: dcbfs [OPTIONS] COMMAND [ARGS]...

	Options:
	  --help  Show this message and exit.

	Commands:
	  delete    Interface for deleting files
	  examine   Interface for examining blocks
	  explore   Show uploaded files
	  init      Initialize dcbfs, if not already initialized
	  retrieve  Interface for retrieving files
	  upload    Interface for uploading files


## Encryption

AES, CBC. (If you want to argue for different encryption, please open an issue.)

## Ledgers

### Giant Ledger

Each entry contains id, location, timestamp of each block; and revocation statements.

(Not currently implemented)

### Personal Ledger

Each publisher has one personal ledger. Its id is a hash of the publisher's secret, and is encrypted with that secret. It is padded to the standard block size. Every time a publisher uploads a file, their personal ledger block is revoked and a new one is added to the giant ledger (blocks don't do updates; they are only created or deleted). They are either timestamped or the id hash is salted with a nonce (still deciding).

Contains the information necessary (filename, number of blocks, derived key; derived key is hash of filename and key) to retrieve, decrypt, and assemble the blocks that form each original file.

Each file must be stored with a unique name.

## Individual Blocks

Each block has padding added to it so they are all the same size. They will have headers which contain the timestamp of when they were last checked and a hash of their id. Blocks are stored on individual machines.

**Header:** 100 bytes: 64 bytes for a sha512 hash of some identifying information, 4 bytes for a timestamp (unix epoch time), 16 bytes for the initialization vector, 16 bytes for a md5 hash of the content (used as checksum)

## Rules for computers participating in the scheme

**Giant Ledger Maintenance:** Computers look at the ledger to check for the existence of block copies, and see which blocks should be copied or deleted. It checks the recorded locations of each block with a slightly old timestamp and updates the ledger if the block is not present in a location. If a block has too few copies or not enough availability (compute an availability score?), it copies it onto itself (if it has space) with a timestamp and records this on the ledger. If a block has been marked as revoked, and the computer finds it on itself, it deletes it from itself (and records this on the ledger).

**Uploading files:** Files are encrypted locally, then split up into standard-sized chunks (with padding if necessary), and each block receives a header (see [Individual Blocks](#individual-blocks)). The order of the blocks' ids are recorded in another block (that is indistinguishable from file blocks), and the id of *that* block is recorded in the user's personal ledger (that also looks like a file block).

**Deleting files:** For a use to delete a file, it issues a revocation statement for all the blocks of the file and the individual file ledger onto the giant ledger. 

**Local Maintenance:** If a computer finds a block on itself with a really old timestamp, it is deleted.

## Communication

Uses HTTPS (chosen for anonymous file transfer and ease of setup)

## Notes

Uses python 2
