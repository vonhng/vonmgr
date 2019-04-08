#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 2.7.10
@author: vonhng
@contact: vonhehe@gmail.com
@file: main.py
@time: 2018/10/11 10:06
"""

from plumbum import cli
from ipmimgr.ipmimgr import Power
from remote_execute.command import Command
from transfer_key.transfer_pubkey import Transfer


class VonMgr(cli.Application):
    PROGNAME = "vonmgr"
    VERSION = "1.0.0"
    #  SUBCOMMAND_HELPMSG = T_("see '{sub} -h/--help' for more info")

    def main(self, *args):
        if args:
            print("Unknown command {0!r}".format(args[0]))
            return 1  # error exit code
        if not self.nested_command:  # will be ``None`` if no sub-command follows
            print("No command given")
            return 1  # error exit code


@VonMgr.subcommand("power")
class Ipmi(Power):
    """check/change power status"""
    pass


@VonMgr.subcommand("add")
class TransferKey(Transfer):
    """transfer key.pub into remote authorized_keys"""
    pass


@VonMgr.subcommand("cmd")
class Cmd(Command):
    """execute cmd in remote node"""
    pass


if __name__ == '__main__':
    VonMgr.run()
