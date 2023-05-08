import json
from http.server import BaseHTTPRequestHandler
from summarizer.integrations.telegram import get_updater, webhook


UPDATER = get_updater()


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        update = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        UPDATER.dispatcher.process_update(update)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        json.dump(self.wfile, {'statusCode': 200, 'body': 'OK'})
        self.wfile.write('Hello, world!'.encode('utf-8'))
        return