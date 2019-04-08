#!/usr/bin/env python
# encoding: utf-8
"""
@version: 2.7.10
@author: vonhng
@contact: vonhehe@gmail.com
@file: power.py
@time: 2018/07/13 09:34
"""
from pyghmi.ipmi import command as ipmi_command
from plumbum import cli, colors

from util.util import print_error, print_ok, print_normal, get_config


class Power(cli.Application):
    """
    远程查看/修改服务器的电源状态，一般针对集群
    """
    VERSION = colors.green | "1.1.0"
    COLOR_GROUPS = {"Meta-switches": colors.bold & colors.yellow, "Switches": colors.green}

    _action, _bmc, _user, _pwd = ("", "", "ADMIN", "123456")

    _get_power = cli.Flag("-g", help="if given, get power status")
    _all = cli.Flag(["-a", "--all"], excludes=["-i", "-u", "-p"], help="handle all nodes")

    @cli.switch("-s", cli.Set("on", "off", "reset", case_sensitive=True), excludes=["-g"], help="set power on|off|reset")
    def set_power(self, cmd):
        self._action = cmd

    @cli.switch("-i", str, help="IPMI IP,example: 111(only 10.10.90.111)/10.10.xxx.xxx")
    def get_ip(self, ip):
        if ip.isdigit():
            bmc = "10.10.90.{}".format(int(ip))
        else:
            bmc = ip
        self._bmc = bmc

    @cli.switch("-p", str, requires=["-u"], help="IPMI PASSWORD,default: 123456")
    def get_pwd(self, pwd):
        self._pwd = pwd

    @cli.switch("-u", str, help="IPMI USER,default: ADMIN", requires=["-i", "-p"])
    def get_user(self, user):
        self._user = user

    def handle_power(self, ip, is_ipmi=False):
        if is_ipmi:
            bmc = ip
        else:
            a = ip.split(".")
            last_ = [str(int(a[-1]) + 100)]
            bmc = ".".join(a[:3] + last_)
        print_normal("[ IPMIINFO ] ipmiip: {}, ipmiuser: {}, ipmipwd: {}".format(bmc, self._user, self._pwd))
        try:
            ipmicmd = ipmi_command.Command(bmc=bmc, userid=self._user, password=self._pwd)
        except Exception:
            print_error("[ ERROR ] failed: not connect")
            return
        if self._get_power:
            try:
                ret = ipmicmd.get_power()
            except Exception as e:
                print_error("[ ERROR ] failed: {}".format(e))
            else:
                print_ok("[ OK ] power is {}".format(ret.get("powerstate", "unknow")))
        else:
            try:
                ret = ipmicmd.set_power(self._action, wait=5)
            except Exception as e:
                print_error("[ ERROR ] failed: {}".format(e))
            else:
                status = ret.get("powerstate") if ret.get("powerstate") else ret.get("pendingpowerstate")
                print_ok("[ OK ] power is {}".format(status, "unknow"))

    def main(self):
        data = get_config()
        if self._all:
            ipmi_ips = data.get("cluster")
            self._user, self._pwd = data.get("ipmi_user"), data.get("ipmi_password")
            is_ipmi = False
        else:
            ipmi_ips = [self._bmc]
            is_ipmi = True
        for i in ipmi_ips:
            self.handle_power(i, is_ipmi)


if __name__ == "__main__":
    Power.run()
