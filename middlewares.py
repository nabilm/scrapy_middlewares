#!/usr/bin/python
# -*-coding:utf-8-*-
"""Scrapy Middleware to set a random User-Agent for every Request.

Downloader Middleware which uses a file containing a list of
user-agents and sets a random one for each request.
"""

import random
from scrapy import signals
from scrapy import log
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.utils.project import get_project_settings


class KippProxy(object):
    def process_request(self, request, spider):
        project_settings = get_project_settings()
        request.meta['proxy'] = project_settings.get('PROXY_SETTINGS')


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, settings, user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                            "Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36"):
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent
        user_agent_list_file = settings.get('USER_AGENT_LIST')
        if not user_agent_list_file:
            # If USER_AGENT_LIST_FILE settings is not set,
            # Use the default USER_AGENT or whatever was
            # passed to the middleware.
            ua = settings.get('USER_AGENT', user_agent)
            self.user_agent_list = [ua]
        else:
            with open(user_agent_list_file, 'r') as f:
                self.user_agent_list = [line.strip() for line in f.readlines()]

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened,
                                signal=signals.spider_opened)
        return obj

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            log.msg("Using user agent (%s) is being used now" % user_agent, level=log.INFO)
            request.headers.setdefault('User-Agent', user_agent)
