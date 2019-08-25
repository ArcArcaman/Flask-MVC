from waitress import serve
import server

if __name__ == '__main__':
    if server.app.config.get("HOST") != None and server.app.config.get("PORT") != None:
        serve(server.app ,host=server.app.config["HOST"], port=server.app.config["PORT"])
    elif server.app.config.get("HOST") == None and server.app.config.get("PORT") != None:
        serve(server.app ,host="localhost", port=server.app.config["PORT"])
    elif server.app.config.get("HOST") != None and server.app.config.get("PORT") == None:
        serve(server.app ,host=server.app.config["HOST"], port=5000)
    else:
        serve(server.app ,host="localhost", port=5000, threads=6)