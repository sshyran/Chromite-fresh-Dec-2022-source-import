This directory contains test data for compdb_no_chroot.py. input/ contains
excerpt of actual compilation_database_chroot.json files. expected/ contains
expected outputs from compdb_no_chroot.py.

When adding a board and a package, it should be selected so that it increases
coverage. For example, amd64-generic represents an x86 board and cherry
represents an ARM board. codelab is the simplest package in platform2 and
cryptohome represents packages having `CROS_WORKON_INCREMENTAL_BUILD=1`.
