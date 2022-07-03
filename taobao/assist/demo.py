#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName     :demo.py
# @Time         :2022/7/2 23:33
# @Author       :Henry Feng
# @Description  :

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    # page.goto("https://www.taobao.com/")
    # 通过淘宝的反爬
    js = """
        Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
        """
    page.add_init_script(js)
    page.goto("https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_20170306")
    page.fill(selector="#fm-login-id", value="15999961458")
    page.fill(selector="#fm-login-password", value="wodetaobao321")
    page.click("#login-form > div.fm-btn > button")
    input()
    browser.close()
