# settings for where to store and access files
# may be configured as the user pleases

import os

# Directory settings
DCBFS_MAIN_DIR = os.path.expanduser('~/.dcbfs/')
TEMP_DIR = DCBFS_MAIN_DIR + 'temp/'
STORAGE_DIR = DCBFS_MAIN_DIR + 'storage/'
OUT_DIR = DCBFS_MAIN_DIR + 'out/'

# This probably won't be a single file in the production version
GIANT_LEDGER_FILE = DCBFS_MAIN_DIR + 'giant_ledger'

KNOWN_HOSTS = []

# BLOCKSIZE must be a multiple of 16, and its unit is bytes
BLOCKSIZE = 512 # will be much larger after testing phase
