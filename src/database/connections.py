import yaml, pyodbc
from abc import ABCMeta, abstractmethod

connection_all:dict = {}
connection_type_list: list = [
    'ODBC'
]

class ConnectionInterface(metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self, conn_name):
        self.connectionstring = ''
        self.conn_name = conn_name
        self.connection = None

    def addToConnectionList(self, conn_name: str, connection: object) -> bool:
        connection_all[conn_name] = connection
        return True

    def create(self, conn_name: str, driver: str, host: str, uid: str, pwd: str, **kwargs):
        pass

    def getCursor(self):
        pass

    def close(self):
        del connection_all[self.__conn_name]
        self.connection.close()
        return True

class ODBCConnections(ConnectionInterface):

    def __init__(self, conn_name):
        super(ODBCConnections, self).__init__(conn_name)

    def addToConnectionList(self, conn_name, connection):
        return super(ODBCConnections, self).addToConnectionList(conn_name, connection)

    def create(self, driver, host, database, uid, pwd, **kwargs):
        self.__connectionstring = "DRIVER={driver};SERVER={host};DATABASE={database};UID={uid};PWD={pwd}".format(driver=driver, host=host, database=database, uid=uid, pwd=pwd)
        
        self.connection = pyodbc.connect(self.__connectionstring, **kwargs)

        if(self.addToConnectionList(self.conn_name, self)):
            return self.connection
        else: 
            return None

    def getCursor(self):
        return self.connection.cursor()
    
    def close(self):
        super(ODBCConnections, self).close()

class ConfigVerifyInterface(metaclass=ABCMeta):
    @abstractmethod
    def verify(self):
        pass

class ODBCConfigVerify(ConfigVerifyInterface):
    def verify(self, connection_conf):
        driver = connection_conf.get('DRIVER')
        host = connection_conf.get('HOST')
        database = connection_conf.get('DB')
        uid = connection_conf.get('USERNAME')
        pwd = connection_conf.get('PASSWORD')
        options = connection_conf.get('OPTIONS')

        if(driver != None and host != None and database != None and uid != None and pwd != None):
            if(driver.strip().strip('{').strip('}') in pyodbc.drivers()):
                return_val = {'driver': driver, 'host': host, 'database': database, 'uid': uid, 'pwd': pwd}
                if(options != None and type(options) == dict):
                    return_val.update(options)
                return return_val
            else:
                raise pyodbc.InterfaceError("Driver not found. Please install the corresponding driver first.")
        else:
            raise ReferenceError("CONFIG ERROR: KEY NOT FOUND")

def version():
    return "0.0"

def __verify(connection_conf):
    conn_type = connection_conf.get('CONNECTION')
    conn_name = connection_conf.get("NAME")

    if(conn_name == None):
        raise ReferenceError("Configuration of NAME is compulsory.")

    if(conn_name in connection_all.keys()):
        raise NameError("Connection name must be unique. Duplicated connection name {}.".format(conn_name))

    if(conn_type == None): raise ReferenceError("Configuration of CONNECTION is compulsory.")

    conn_type = conn_type.upper()

    if(conn_type not in connection_type_list): raise ValueError("Connection type is not defined. It may due to unimplemented type of connection or naming error. Please check the connection name if it is in the following list:\n" + str(connection_type_list))

    elif(conn_type == 'ODBC'):
        return (conn_type, conn_name, ODBCConfigVerify().verify(connection_conf))
     

def connect_all():
    
    connections_read = yaml.load(open("./database/connections.yaml", 'r'), Loader=yaml.FullLoader)

    for connection_conf in connections_read:
        
        verified_conf = __verify(connection_conf)

        if(verified_conf[0] == 'ODBC'):
            ODBCConnections(verified_conf[1]).create(**(verified_conf[2]))

    return connection_all
    
    