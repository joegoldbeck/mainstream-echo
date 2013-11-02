import tornado.ioloop
from tornado.web import asynchronous, RequestHandler
import tornado.httpclient

with open('apikey.txt', 'r') as key_file: # your api key should be stored as the first line of a file named apikey.txt
    api_key = key_file.readline().rstrip('\n')

class MainHandler(RequestHandler):
    @asynchronous
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch('http://developer.echonest.com/api/v4/artist/search?api_key=' + api_key + '&sort=hotttnesss-desc&bucket=hotttnesss&results=10', self._handle_response)
    def _handle_response(self, res):
        if res.error:
            self.write("Error")
            print "Error:", res.error
        else:
            self.write("Success")
            print "Success"
        self.finish()

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(5000)
    tornado.ioloop.IOLoop.instance().start()
