import json
import urllib
from http.server import BaseHTTPRequestHandler
from summarizer.integrations.telegram import get_updater, webhook


UPDATER = get_updater()


class handler(BaseHTTPRequestHandler):
    def send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"statusCode": status_code, "body": data}).encode('utf-8'))

    def do_POST(self):
        query = urllib.parse.urlparse(self.path).query
        query_params = urllib.parse.parse_qs(query)
        if 'token' in query_params:
            caller_token = query_params['token'][0]
        else:
            self.send_json_response(400, 'Missing `token` parameter')
            return

        if caller_token != UPDATER.bot.token:
            self.send_json_response(403, 'Forbidden')
            return
        
        try:
            update = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        except:
            self.send_json_response(400, 'Invalid JSON')
            return
        response = webhook(UPDATER.dispatcher, update)
        self.send_json_response(200, response)
        return