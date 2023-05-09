import json
import urllib
from http.server import BaseHTTPRequestHandler
from summarizer.integrations.telegram import get_updater, webhook


UPDATER = get_updater()


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        query = urllib.parse.urlparse(self.path).query
        query_params = urllib.parse.parse_qs(query)
        if 'token' in query_params:
            caller_token = query_params['token'][0]
        else:
            self.send_response(400)
            self.end_headers()
            json.dump({'statusCode': 403, 'body': 'Missing `token` parameter'}, self.wfile)
            return

        if caller_token != UPDATER.bot.token:
            self.send_response(403)
            self.send_header('Content-type','application/json')
            self.end_headers()
            json.dump({'statusCode': 403, 'body': 'Forbidden'}, self.wfile)
            return
        update = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        response = webhook(UPDATER.bot, update)
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        json.dump(response, self.wfile)
        return