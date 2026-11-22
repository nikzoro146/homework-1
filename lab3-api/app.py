import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


ITEMS = [
    {"id": 1, "title": "Основы Linux", "topic": "linux"},
    {"id": 2, "title": "Навигация в терминале", "topic": "linux"},
    {"id": 3, "title": "Управление пакетами", "topic": "linux"},
    {"id": 4, "title": "Введение в контейнеры", "topic": "podman"},
    {"id": 5, "title": "Сборка образов", "topic": "podman"},
    {"id": 6, "title": "Основы Python", "topic": "python"},
    {"id": 7, "title": "Продвинутый Podman", "topic": "podman"} # 7-я запись
]

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        if path == '/health':
            self._send_json(200, {"status": "ok"})
            
        elif path == '/api/items':
            topic_filter = query.get('topic', [None])[0]
            if topic_filter:
                filtered_items = [item for item in ITEMS if item['topic'] == topic_filter]
            else:
                filtered_items = ITEMS
            self._send_json(200, {"items": filtered_items})
            
        elif path == '/api/summary':
            total = len(ITEMS)
            by_topic = {}
            for item in ITEMS:
                topic = item['topic']
                by_topic[topic] = by_topic.get(topic, 0) + 1
            self._send_json(200, {"total": total, "by_topic": by_topic})
            
        else:
            self._send_json(404, {"error": "Not found"})

    def _send_json(self, status, data):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        print(f"[LOG] {self.address_string()} - {format % args}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    host = os.environ.get('HOST', '127.0.0.1')
    print(f"Сервер запущен на http://{host}:{port}")
    server = HTTPServer((host, port), APIHandler)
    server.serve_forever()