#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 2.7.10
@author: vonhng
@contact: qianyong.feng@woqutech.com
@file: util.py
@time: 2018/10/11 12:30
"""

import subprocess
import paramiko
from plumbum import colors


class SSHError(Exception):
    pass


class SSHClient(paramiko.SSHClient):
    max_read_size = 102400

    def exec_command(self, command, bufsize=-1, timeout=None, get_pty=False):
        stdin, stdout, stderr = super(SSHClient, self).exec_command(command, bufsize, timeout, get_pty)
        stdin.close()
        stdin.flush()

        err = stderr.read()
        output = stdout.read()
        if err:
            raise SSHError(err)
        else:
            return output


class SSH(object):
    def __init__(self, host, username, password,  port=22):
        self.host = host
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, port, username, password, timeout=2)

    def exec_command(self, command, bufsize=-1, timeout=None, get_pty=False):
        return self.ssh.exec_command(command, bufsize, timeout, get_pty)

    def close(self):
        self.ssh.close()


def run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=False)
    except Exception as e:
        raise Exception(
            "Run cmd %s failed: %s" % (" ".join(cmd), e))
    return output


def print_error(msg):
    print colors.red | msg


def print_ok(msg):
    print colors.green | msg


def print_normal(msg):
    print colors.bold | msg