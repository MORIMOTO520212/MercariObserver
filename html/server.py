import http.server
import socketserver

port = 8080

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", port), Handler) as httpd:
    print("add Item> http://localhost:{}/addItem".format(port))
    httpd.serve_forever()