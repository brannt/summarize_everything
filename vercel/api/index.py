import json
from http.server import BaseHTTPRequestHandler
from summarizer.integrations.telegram import get_updater, webhook


UPDATER = get_updater()


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        caller_token = self.path.split('/')[-1]
        if caller_token != UPDATER.bot.token:
            self.send_response(403)
            self.send_header('Content-type','application/json')
            self.end_headers()
            json.dump(self.wfile, {'statusCode': 403, 'body': 'Forbidden'})
            self.wfile.write('Hello, world!'.encode('utf-8'))
            return
        update = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        response = webhook(UPDATER.bot, update)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        json.dump(self.wfile, response)
        return