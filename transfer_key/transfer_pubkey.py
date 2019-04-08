#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 2.7.10
@author: vonhng
@contact: vonhehe@gmail.com
@file: transfer_pubkey.py
@time: 2018/7/13
"""

from plumbum import cli, colors
from util.util import SSH, print_error, print_ok, run_cmd, get_config


class Transfer(cli.Application):
    """上传本地的公钥到远程服务器，一般针对集群"""
    VERSION = colors.bold | "1.1.0"
    COLOR_GROUPS = {"Meta-switches": colors.bold & colors.yellow, "Switches": colors.bold & colors.yellow}

    _user, _pwd, _ips = ("root", "XXXXXX", "")  # 这里修改默认用户和密码
    _all = cli.Flag(["-a", "--all"], excludes=["-i", "-u", "-p"], help="handle all nodes")

    @cli.switch(["-i", "-ip"], str, help="remote ips,use '/' to split")
    def ips(self, ips):
        self._ips = ips

    @cli.switch(["-u", "--user"], str, help="user")
    def user(self, user):
        self._user = user

    @cli.switch(["-p", "--password"], str, help="password")
    def pwd(self, pwd):
        self._pwd = pwd

    def main(self):
        data = get_config()
        pubkey_path = data.get("pubkey_path")
        pubkey = run_cmd(["cat", pubkey_path])

        cmd = "echo '{}' >> /root/.ssh/authorized_keys".format(pubkey)
        if self._all:
            remote_ips = data.get("cluster")
            self._user, self._pwd = data.get("user"), data.get("password")
        else:
            remote_ips = self._ips.split("/")
        for remote_ip in remote_ips:
            try:
                ssh = SSH(remote_ip, self._user, password=self._pwd, port=data.get("port"))
                ssh.exec_command(cmd)
                ssh.close()
            except Exception as e:
                print_error("[ ERROR ] {}".format(e))
            else:
                print_ok("[ OK ] transfer pubkey --> {}".format(remote_ip))


if __name__ == '__main__':
    Transfer.run()
