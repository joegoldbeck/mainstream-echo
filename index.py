import tornado.ioloop
from tornado.web import asynchronous, RequestHandler
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.escape import json_encode, json_decode
from urllib import urlencode
import uuid

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

class ArtistsHandler(RequestHandler):
    @gen.coroutine
    def get(self): # THIS IS TEMPORARY TO PLAY AROUND WITH
        # create_profile_res = yield create_profile()
        # profile_id = extract_profile_id(create_profile_res.body)
        profile_id = 'CAYBDAK1421BD0AC59'
        artists = ['Britney Spears', 'Radiohead', 'The Beatles']
        add_artists_res = yield add_artists(profile_id, artists)
        ticket = extract_ticket(add_artists_res.body)
        print {'ticket' : ticket, 'profile_id': profile_id}
        self.write({'ticket' : ticket, 'profile_id': profile_id})

    @gen.coroutine
    def post(self):
        artists = json_decode(self.get_argument('artists'))
        print artists[1] #TEST STATEMENT
        create_profile_res = yield create_profile()
        profile_id = extract_profile_id(create_profile_res.body)
        add_artists_res = yield add_artists(profile_id, artists)
        ticket = extract_ticket(add_artists_res.body)
        self.write({'ticket' : ticket, 'profile_id': profile_id})

@gen.coroutine
def get_artists():
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(
            'http://developer.echonest.com/api/v4/artist/search?api_key=' +
            api_key + '&sort=hotttnesss-desc&bucket=hotttnesss&results=10')
    raise gen.Return(response)


@gen.coroutine
def create_profile():
    req_url = 'http://developer.echonest.com/api/v4/catalog/create'
    req_body = urlencode({'api_key': api_key, 'format': 'json',
                            'name': uuid.uuid1().hex, 'type': 'artist'}) # random name for now
    req = HTTPRequest(req_url, method='POST', body=req_body)
    http_client = AsyncHTTPClient()
    res = yield http_client.fetch(req)
    raise gen.Return(res)


@gen.coroutine
def add_artists(profile_id, artists):
    req_url = 'http://developer.echonest.com/api/v4/catalog/update'
    data = (artists_to_items(artists))
    req_body = urlencode({'api_key': api_key, 'format': 'json', 'id': profile_id, 'data': data, 'data_type': data})
    headers = {'Content-Type': 'application/json; charset=UTF-8'}

    req = HTTPRequest(req_url, method='POST', headers = headers, body=req_body)
    http_client = AsyncHTTPClient()
    res = yield http_client.fetch(req)
    raise gen.Return(res)


def extract_profile_id(body):
    parsed = json_decode(body)
    return parsed['response']['id']

def extract_ticket(body):
    parsed = json_decode(body)
    return parsed['response']['ticket']

def artists_to_items(artists):
    print artists
    return [{'item': {'item_id': i, 'artist_name': artist}} for i, artist in enumerate(artists)]


application = tornado.web.Application([
    (r'/', MainHandler), # GET webpage
    (r'/artists', ArtistsHandler), # POST the artists list and store id & ticket in cookie
    # (r'/status', StatusHandler), # GET the status of the profile
    # (r'/results', ResultsHandler) # GET the results summary
])

if __name__ == '__main__':
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
