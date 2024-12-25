from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader
import urllib.parse
import os

# Инициализация Jinja2
env = Environment(loader=FileSystemLoader('templates'))

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def render_template(self, template_name, context=None):
        if context is None:
            context = {}
        template = env.get_template(template_name)
        return template.render(context).encode('utf-8')
    
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = self.render_template("index.html")
            self.wfile.write(html)
        elif self.path == "/form":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = self.render_template("form.html")
            self.wfile.write(html)
        elif self.path.startswith("/static/"):
            self.handle_static()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Страница не найдена".encode('utf-8'))


def handle_static(self):
    static_file_path = self.path.lstrip("/")
    try:
        if os.path.exists(static_file_path):
            content_type = "text/css" if static_file_path.endswith(".css") else "image/jpeg"
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            with open(static_file_path, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Файл не найден".encode('utf-8'))
    except Exception as e:
        self.send_response(500)
        self.end_headers()
        self.wfile.write(f"Ошибка: {e}".encode('utf-8'))

    
    def do_POST(self):
        if self.path == "/form":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            name = post_data.get('name', [''])[0]
            phone_model = post_data.get('phone_model', [''])[0]
            issue = post_data.get('issue', [''])[0]

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            response = self.render_template("success.html", context={
                "name": name,
                "phone_model": phone_model,
                "issue": issue
            })
            self.wfile.write(response)

# Запуск сервера
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на порту {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
