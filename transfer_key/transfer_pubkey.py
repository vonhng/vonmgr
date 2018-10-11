#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 2.7.10
@author: vonhng
@contact: vonhng@qq.com
@file: transfer_pubkey.py
@time: 2018/7/13
"""
import os
from plumbum import cli, colors

from util.util import SSH, print_error, print_ok


class Transfer(cli.Application):
    """上传本地的公钥到远程服务器，一般针对集群"""
    VERSION = colors.bold | "1.0.0"
    COLOR_GROUPS = {"Meta-switches": colors.bold & colors.yellow, "Switches": colors.bold & colors.yellow}

    _user, _pwd, _ips = ("root", "cljslrl0620", "")  # 这里修改默认用户和密码

    @cli.switch(["-i", "-ip"], str, mandatory=True, help="remote ips,use '/' to split")
    def ips(self, ips):
        self._ips = ips

    @cli.switch(["-u", "--user"], str, help="user")
    def user(self, user):
        self._user = user

    @cli.switch(["-p", "--password"], str, help="password")
    def pwd(self, pwd):
        self._pwd = pwd

    def main(self):
        try:
            pubkey = os.environ["PUBKEY_PATH"]
        except KeyError as e:
            print_error("[ ERROR ] Please export {}".format(e))
            return
        cmd = "echo '{}' >> /root/.ssh/authorized_keys".format(pubkey)
        remote_ips = self._ips.split("/")
        for remote_ip in remote_ips:
            try:
                ssh = SSH(remote_ip, self._user, password=self._pwd, port=22)
                ssh.exec_command(cmd)
                ssh.close()
            except Exception as e:
                print_error("[ ERROR ] {}".format(e))
            else:
                print_ok("[ OK ] transfer pubkey --> {}".format(remote_ip))


if __name__ == '__main__':
    Transfer.run()
