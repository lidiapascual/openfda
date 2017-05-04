import socketserver
import web


PORT=8003

Handler=web.testHTTPRequestHandler

httpd=socketserver.TCPServer(('',PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
