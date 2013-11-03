import tornado.ioloop
from tornado.web import asynchronous, RequestHandler
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.escape import json_encode, json_decode
from urllib import urlencode

# your api key should be stored as the first line of a file named apikey.txt
with open('apikey.txt', 'r') as key_file:
    api_key = key_file.readline().rstrip('\n')


class MainHandler(RequestHandler):
    def get(self):
        self._reply()
    def _reply(self):
        print self.request.method
        self.write('There should be a webpage here')
        self.finish()

class HowMainstreamHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        artists = ['Britney+Spears', 'Radiohead', 'The+Beatles'] # Temporarily hardcoded
        get_profile_responses = yield [get_artist_profile(artist) for artist in artists]
        artistProfiles = [json_decode(response.body)['response']['artist'] for
                response in get_profile_responses]
        hotttnesss = [profile['hotttnesss'] for profile in artistProfiles]
        familiarity = [profile['familiarity'] for profile in artistProfiles]
        print {'hotttnesss' : hotttnesss, 'familiarity': familiarity}
        self.write({'hotttnesss' : hotttnesss, 'familiarity': familiarity})

@gen.coroutine
def get_artist_profile(artist):
    req_url = ('http://developer.echonest.com/api/v4/artist/profile?api_key=' + api_key +
            '&name=' + artist + '&bucket=familiarity&bucket=hotttnesss')
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(req_url)
    raise gen.Return(response)


application = tornado.web.Application([
    (r'/', MainHandler), # GET webpage
    (r'/how_mainstream', HowMainstreamHandler)
])

if __name__ == '__main__':
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
