# -*- coding: utf-8 -*-
import re
import urllib

import requests

from ..configure.config import logger
from ..configure import config

# google api
from ..configure  import tools as sptools


def googletrans(text, src, dest):
    url = f"https://translate.google.com/m?sl={urllib.parse.quote(src)}&tl={urllib.parse.quote(dest)}&hl={urllib.parse.quote(dest)}&q={urllib.parse.quote(text)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    proxies = None
    if config.video['proxy']:
        proxies = {
            'http': config.video['proxy'],
            'https': config.video['proxy']
        }
    try:
        response = requests.get(url, proxies=proxies, headers=headers, timeout=40)
        print(f"code==={response.status_code}")
        if response.status_code != 200:
            sptools.set_process(f"[error] google翻译失败 status_code={response.status_code}")
            return f"[error] translation code={response.status_code}"
        re_result = re.findall(
            r'(?s)class="(?:t0|result-container)">(.*?)<', response.text)
    except Exception as e:
        logger.error(f"google translate error:" + str(e))
        sptools.set_process(f"[error]google 翻译失败:请确认能连接到google" + str(e))
        return "[error] google api Please check the connectivity of the proxy or consider changing the IP address."
    if len(re_result)<1:
        sptools.set_process('[error]google翻译失败了')
        return "[error] on translation"
    return re_result[0]
