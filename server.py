#PROGRAMA PRINCIPAL
import socketserver
import web

##
#WEB SERVER
##
#web es el fichero donde esta guardada
PORT=8001 #A partir de 1024
#clase a partir de la cual se crean objetos
#Handler=http.server.SimpleHTTPRequestHandler
Handler=web.testHTTPRequestHandler

httpd=socketserver.TCPServer(('',PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

#Handler es la clase a traves d
