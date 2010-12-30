#!/bin/bash
#
# Run the backup and move the tarball to a remote sever.
#
# This is just an example.

export PYTHONPATH="./src"

REMOTE="daniel@example.com"


python backup.py

# Optionally encrypt the data here before sending


ssh $REMOTE SBUrotate
scp ~/backup/dn-laptop.0.tar.bz2 $REMOTE:~/backup
