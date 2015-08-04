#!/usr/bin/env python3
import getpass
import pathlib
import subprocess
import sys

from yaml import load


def call(command):
    return call_with_user(command, getpass.getuser())

def call_with_user(command, user):
    command += sys.argv[1:]
    if getpass.getuser() != user:
        command = ['sudo', '-u' + user] + command
    return subprocess.call(command)

if __name__ == '__main__':
    file_path = pathlib.Path(__file__)
    command = file_path.parts[-1]
    script_name = file_path.resolve().parts[-1]
    if command == script_name:
        print('''
This script was not intended to run standalone. You should create and edit the
config file which is named 'config.yaml' (without the quotes) and located where
this script is located, which contains the commands intended to be executed.

The file would be like this:

command-name:
    command: [an, array, of, commandline, which, would, be, passed, to,'''
    ''' subprocess, module]
    user: name-of-user-to-be-executed-with

Then, you should create a symbolic link of this script ({}), named as the
command name you configured in the config file:

ln -s {} command-name

And then you will be able to execute the command with the symlink you created.
Make sure that this script is executable.
        '''.strip().format(script_name, file_path.resolve()))
        sys.exit(126)
    config_path = pathlib.Path(__file__).resolve().parent / 'config.yaml'
    with (config_path).open('r') as r:
        commands = load(r)
    if command in commands:
        if 'command' in commands[command]:
            if 'user' in commands[command]:
                sys.exit(call_with_user(
                    commands[command]['command'],
                    commands[command]['user']
                ))
            else:
                sys.exit(call(commands[command]['command']))
        else:
            print(
                'Looks like the command \'{}\' is not configured correctly in'
                'your configuration. Please check the config file in {} .'
                .format(command, config_path)
            )
            sys.exit(126)
    else:
        print(
            'Command {} is not defined in config; Please define it in {} .'
            .format(command, config_path)
        )
