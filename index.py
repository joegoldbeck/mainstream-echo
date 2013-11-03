import tornado.ioloop
from tornado.web import asynchronous, RequestHandler
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_encode, json_decode

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
        res = yield get_artists()
        if res.error:
            self.send_error(500)
            print(res.error)
            return
        self.write(res.body)

    @gen.coroutine
    def post(self):
        create_profile_res = yield create_profile()
        if create_profile_res.error:
            self.send_error(500)
            print 'Error creating profile: ' + create_profile_res.error
            return
        profile_id = extract_profile_id(create_profile_res)
        artists = ['Britney Spears', 'Radiohead', 'The Beatles']
        add_artists_res = yield add_artists(profile_id, artists)
        if add_artists_res.error:
            self.send_error(500)
            print('Error adding artists: ' + add_artists_res.error)
            return
        ticket = extract_ticket(add_artists_res)


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
    req_body = json_encode({'api_key': api_key, 'format': 'json',
                            'name': 'User\'s Favorite Artists', 'type': 'artist'})
    req = {'method': 'POST', 'url': req_url, 'body': 'req_body'}
    http_client = AsyncHTTPClient()
    res = yield http_client.fetch(req)
    raise gen.Return(res)


@gen.coroutine
def add_artists(profile_id, artists):
    req_url = 'http://developer.echonest.com/api/v4/catalog/update'
    data = json_encode(artists_to_items(artists))
    req_body = json_encode({'api_key': api_key, 'format': 'json', 'id': profile_id, 'data': data})
    req = {'method': 'POST', 'url': req_url, 'body': 'req_body'}
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
    return [{'item_id': i, 'artist_name': artist} for i, artist in enumerate(artists)]


application = tornado.web.Application([
    (r'/', MainHandler), # GET webpage
    (r'/artists', ArtistsHandler), # POST the artists list and store id & ticket in cookie
    # (r'/status', StatusHandler), # GET the status of the profile
    # (r'/results', ResultsHandler) # GET the results summary
])

if __name__ == '__main__':
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
