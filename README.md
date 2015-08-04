call-with-user-wrapper
======================

This script is a simple wrapper around the command line: it just executes
other commands with arguments, optionally always with the specified user.

The script has to be configured with a file named config.yaml which should
dwell in the same directory as the script is. After configuration, a symlink
should be created and executed accordingly to utilize the script.
