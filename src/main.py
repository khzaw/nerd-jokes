#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
template.register_template_library('utils.custom_filters')
import twitter
import os


HASHTAG = '#nerdjokes'
RESULTS_PER_PAGE = 20

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {'tweets' : crawl_page()}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

twitter_search = twitter.Twitter(domain='search.twitter.com')

def crawl_page(page=1):
    searched_results = twitter_search.search(q=HASHTAG, rpp=RESULTS_PER_PAGE, page=page)['results']
    final_result = [
            {
                'created_at' : result['created_at'], 
                'text' : result['text'],
                'username' : result['from_user'],
                'real_name' : result['from_user_name'],
                'profile_pic' : result['profile_image_url'],
            } for result in searched_results]
    return final_result

def main():
    application = webapp.WSGIApplication(
                    [('/', MainPage)],
                debug=True)
    run_wsgi_app(application)




if __name__ == '__main__':
    main()
