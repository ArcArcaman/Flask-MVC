import json

def serverImport(join=True, from_path="../service.cfg"):
    with open(from_path) as config:
        conf = json.load(config)
        servers = conf["server"]
        server_dict = dict()
        if join == True:
            for server in servers:
                server_dict[server["name"]] = {k: v for k, v in server.items() if k != "name"}
                server_dict[server["name"]].update(url = server["host"] + ':' + str(server["port"]))
        else:
            for server in servers:
                server_dict[server["name"]] = {k: v for k, v in server.items() if k != "name"}
    return server_dict

def getURL(server_dict, name):
    return server_dict.get(name).get("url")

# if __name__ == "__main__":
#     print(serverImport(join=True))