#!/usr/bin/env python

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import uuid

from datetime import datetime
from locust import TaskSet, task
from locust.contrib.fasthttp import FastHttpLocust
from bs4 import BeautifulSoup


class MetricsTaskSet(TaskSet):
    _deviceid = None

    def on_start(self):
        self._deviceid = str(uuid.uuid4())

    @task
    def wordpress(self):
        self.client.get('/wordpress')
        # response = self.client.get('/wordpress')
        # self.get_linked_assets(response.text)

    # parse HTML and get any script and stylehseet assets
    def get_linked_assets(self, responsetext):
        soup = BeautifulSoup(responsetext, "html.parser")
        resource_urls = set()
        for tag in soup.find_all('script', attrs = {'src': True}):
            resource_urls.add(tag['src'])
        for tag in soup.find_all('link', attrs = {'rel': 'stylesheet', 'href': True}):
            resource_urls.add(tag['href'])
        for url in resource_urls:
            if self.is_on_site(url):
                self.client.get(url, name = url)

    # check if url is on target WordPress site and not elsewhere on the internet
    def is_on_site(self, url):
        if '/wordpress/wp-content/' in url:
            return True
        elif '/wordpress/wp-includes/' in url:
            return True
        else:
            return False


class MetricsLocust(FastHttpLocust):
    task_set = MetricsTaskSet
