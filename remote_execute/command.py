#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 2.7.10
@author: vonhng
@contact: qianyong.feng@woqutech.com
@file: command.py
@time: 2018/10/11 12:51
"""
from plumbum import cli, colors

from util.util import SSH, print_error, print_ok, print_normal


class Command(cli.Application):
    """
    远程执行命令，一般针对集群
    """
    VERSION = colors.bold | "1.0.0"
    COLOR_GROUPS = {"Meta-switches": colors.bold & colors.yellow, "Switches": colors.bold & colors.yellow}

    _user, _pwd = ("root", "cljslrl0620")  # 这里修改默认用户和密码
    _ips, _cmd = ("", "")
    no_log = cli.Flag("--no-log", help="if given, print detail")

    @cli.switch(["-i", "--ip"], str, help="remote ips,use '/' to split")
    def ips(self, ips):
        self._ips = ips

    @cli.switch(["-u", "--user"], str, help="user")
    def user(self, user):
        self._user = user

    @cli.switch(["-p", "--password"], str, help="password")
    def pwd(self, pwd):
        self._pwd = pwd

    def main(self):
        cmd = raw_input("please input cmd:")
        remote_ips = self._ips.split("/")
        for remote_ip in remote_ips:
            try:
                ssh = SSH(remote_ip, self._user, password=self._pwd, port=22)
                result = ssh.exec_command(cmd)
                ssh.close()
            except Exception as e:
                print_error("[ ERROR ] {}".format(e))
            else:
                if self.no_log:
                    print_ok("[ OK ] execute at {0} ".format(remote_ip))
                else:
                    print_ok("[ OK ] {0} result: {1} {0}".format("="*10, remote_ip))
                    print_normal(result)

