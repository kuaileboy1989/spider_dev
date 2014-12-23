#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os

def get_config():
    ret = {}

    config = ConfigParser.ConfigParser()
    config.read('config.py')
    for item in config.sections():
        tmp_dict = {}
        for k,v in config.items(item):
            tmp_dict[k] = v

        ret[item] = tmp_dict

    return ret

if __name__ == "__main__":
    print get_config()
