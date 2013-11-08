import os
import tornado.ioloop
from tornado.web import asynchronous, RequestHandler
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.escape import json_encode, json_decode, squeeze
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
        artists = [squeeze(artist).replace(' ', '+') for artist in self.get_arguments('artist') if artist]
        get_profile_responses = yield [get_artist_profile(artist) for artist in artists]
        decoded_response_bodies = [json_decode(response.body) for response in get_profile_responses]
        artist_profiles = format_artist_profiles(decoded_response_bodies)
        self.render('mainstream.html', snark=(how_mainstream(artist_profiles)))

@gen.coroutine
def get_artist_profile(artist):
    req_url = ('http://developer.echonest.com/api/v4/artist/profile?api_key=' + api_key +
            '&name=' + artist + '&bucket=familiarity&bucket=hotttnesss')
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(req_url)
    raise gen.Return(response)

def format_artist_profiles(response_bodies):
    response_dicts = [response_body['response'] for response_body in response_bodies]
    return [response['artist'] for response in response_dicts if 'artist' in response]

def how_mainstream(artist_profiles):
    if not artist_profiles:
        return 'Reply hazy try again'
    hotttnessses = [profile['hotttnesss'] for profile in artist_profiles]
    familiaritys = [profile['familiarity'] for profile in artist_profiles]
    median_hot, median_fam = (median(hotttnessses), median(familiaritys))
    if median_hot > 0.75 and median_fam > 0.75:
        return 'You may rely on it'
    elif median_hot > 0.75 and median_fam <= 0.75:
        return 'Outlook good'
    elif median_hot <= 0.75 and median_fam > 0.75:
        return 'As I see it yes'
    elif median_hot < 0.5 or median_fam < 0.5:
        return 'Outlook not so good' # subtext burn
    else:
        return 'My sources say no'


application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/how_mainstream', HowMainstreamHandler)
])

if __name__ == '__main__':
    application.listen(os.environ.get('PORT', 5000))
    tornado.ioloop.IOLoop.instance().start()
