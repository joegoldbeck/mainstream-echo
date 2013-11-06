import os
import tornado.ioloop
from tornado.web import asynchronous, RequestHandler
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.escape import json_encode, json_decode
from urllib import urlencode
from numpy import median

# your api key should be stored in the environment
api_key = os.environ.get('ECHONEST_KEY')


class IndexHandler(RequestHandler):
    def get(self):
        self.render('index.html')


class HowMainstreamHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        artists = [artist.strip().replace(' ', '+') for artist in self.get_arguments('artist') if artist] # could also use regex re.sub(r'\s+', '+', artist.strip()) to be even safer
        get_profile_responses = yield [get_artist_profile(artist) for artist in artists]
        decodedResponses = [json_decode(response.body)['response'] for response in get_profile_responses]
        artistProfiles = [response['artist'] for response in decodedResponses if 'artist' in response]
        self.write(how_mainstream(artistProfiles))

@gen.coroutine
def get_artist_profile(artist):
    req_url = ('http://developer.echonest.com/api/v4/artist/profile?api_key=' + api_key +
            '&name=' + artist + '&bucket=familiarity&bucket=hotttnesss')
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(req_url)
    raise gen.Return(response)

def how_mainstream(artistProfiles):
    hotttnessses = [profile['hotttnesss'] for profile in artistProfiles]
    familiaritys = [profile['familiarity'] for profile in artistProfiles]
    median_hot, median_fam = (median(hotttnessses), median(familiaritys))
    return {'hot': median_hot, 'fam': median_fam}


application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/how_mainstream', HowMainstreamHandler)
])

if __name__ == '__main__':
    application.listen(os.environ.get('PORT', 5000))
    tornado.ioloop.IOLoop.instance().start()
