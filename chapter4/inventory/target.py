#!/usr/bin/env python3
""" target inventory script """

import argparse
import io
import json
import subprocess
import sys

import paramiko


def parse_args():
    """command-line options"""
    parser = argparse.ArgumentParser(description="target inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')
    return parser.parse_args()


def list_running_hosts():
    """target.py --list function"""
    cmd = ["target", "status", "--machine-readable"]
    status = subprocess.check_output(cmd).rstrip().decode("utf-8")
    hosts = []
    for line in status.splitlines():
        (_, host, key, value) = line.split(',')[:4]
        if key == 'state' and value == 'running':
            hosts.append(host)
    return hosts


def get_host_details(host):
    """target.py --host <hostname> function"""
    cmd = ["target", "ssh-config", host]
    ssh_config = subprocess.check_output(cmd).decode("utf-8")
    config = paramiko.SSHConfig()
    config.parse(io.StringIO(ssh_config))
    host_config = config.lookup(host)
    return {'ansible_host': host_config['hostname'],
            'ansible_port': host_config['port'],
            'ansible_user': host_config['user'],
            'ansible_private_key_file': host_config['identityfile'][0]}


def main():
    """main"""
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        json.dump({'target': hosts}, sys.stdout)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)


if __name__ == '__main__':
    main()
