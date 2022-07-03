#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName     :cookies.py
# @Time         :2022/7/3 15:15
# @Author       :Henry Feng
# @Description  :
import json


def get_cookies(path):
    with open(path, 'r') as file:
        cookie_list = json.load(file)
    return cookie_list


def set_cookies(cookies, path):
    with open(path, 'w') as file:
        json.dump(cookies, file)
