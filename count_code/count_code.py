#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 2.7.10
@author: vonhng
@contact: qianyong.feng@woqutech.com
@file: count_code.py
@time: 2018/10/11 13:48
"""
import os
from collections import defaultdict
from plumbum import cli, colors

from util.util import print_ok


class CountCode(cli.Application):
    """
    统计本地文件夹/文件的代码行数
    """
    VERSION = colors.bold | "1.0.0"
    COLOR_GROUPS = {"Meta-switches": colors.bold & colors.yellow, "Switches": colors.bold & colors.yellow}

    _path = os.getcwd()  # 这里当前目录
    _need_type_list = ['yaml', 'py', 'yml', 'go', 'sh']  # 指定想要统计的文件类型
    no_log = cli.Flag("--no-log", help="if given, print detail")

    @cli.switch(["-p", "--path"], str, help="directory path")
    def path(self, path):
        self._path = path

    def _get_all_file(self):
        file_dicts = defaultdict(list)
        for parent, dir_names, file_names in os.walk(self._path):
            for filename in file_names:
                file_type = filename.split('.')[-1]
                # 只统计指定的文件类型，略过一些log和cache文件
                if file_type in self._need_type_list:
                    file_dicts[file_type].append(os.path.join(parent, filename))
        return file_dicts

    def main(self):
        d = {}
        file_dicts = self._get_all_file()
        # 统计一个文件的行数
        for file_type, file_lists in file_dicts.iteritems():
            d[file_type] = 0
            for fname in file_lists:
                count = 0
                with open(fname, 'r') as f:
                    for file_line in f.readlines():
                        if file_line != '' and file_line != '\n':  # 过滤掉空行
                            count += 1
                    if not self.no_log:
                        print fname + '----', count
                    d[file_type] += count

        print_ok("[ OK ]  total lines:", sum(d.values()))

