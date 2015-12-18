import json
import os.path
import logging
import re
from pymongo import MongoClient

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))
DATASET_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dataset'))

"""
    Attributes:
    __config_path: string; keep relative path to the config file
    __isConnected: boolean; show status of database client connection
    __db: YLPDBCoordinator
"""


class DBConnector:
    def __init__(self, config_path, db_name='test'):
        self.__config_path = config_path
        self.__isConnected = False
        self.__db = None
        self.__client = None
        self.__databases = dict()
        self.__dbName = db_name

    def connect(self):
        if self.database_path is None:
            return False

        if self.__isConnected:
            return self.__isConnected

        with open(self.database_path) as json_file:
            config = json.load(json_file)

        host = config['db']['host']
        port = config['db']['port']
        url = "mongodb://{}:{}".format(host, port)
        self.__client = MongoClient(url)
        self.__isConnected = True

        return self.__isConnected

    def disconnect(self):
        self.__client.close()
        self.__client = None
        self.__isConnected = False

    def get_database_name(self, db_name='test', collection_name='yelps'):
        if not self.__isConnected:
            print "Error !! The database have not been connected. Call 'connect()' before using it"
            return None

        key = db_name + ':' + collection_name
        db = self.__databases.get(key, None)
        if db == None:
            # create new coordinator and save to databases dic
            newDB = self.__client[db_name][collection_name]
            coordinator = DBCoordinator(newDB)
            db = coordinator
            self.__databases[key] = db

        return db

    def reset_database_name(self, db_name='test', collection_name='yelps'):
        collection = self.__client[db_name][collection_name]
        return collection.drop()

    @property
    def database_path(self):
        return self.__config_path

    @database_path.setter
    def database_path(self, path):
        self.__config_path = path


"""
    Attributes:
    __client: MongoClient
"""


class DBCoordinator:
    def __init__(self, db):
        self.__db = db
        self.__bulk = None

    def openBulk(self):
        self.__bulk = self.db.initialize_unordered_bulk_op()

    def addToBulk(self, obj):
        self.__bulk.insert(obj)

    def closeBulk(self):
        return self.__bulk.execute()

    def addObject(self, obj):
        print(type(obj))
        return self.addObjects([obj])

    def removeObject(self, objId):
        pass

    def addObjects(self, objs):
        insertedObjects = []
        for obj in objs:
            insertedObjects.append(obj.val)

        res = self.db.insert_many(insertedObjects)
        results = []
        for objId in res.inserted_ids:
            results.append(str(objId))

        return results

    def removeObjects(self, *objIds):
        pass

    def find(self, predicate={}):
        res = []
        cursor = self.db.find(predicate)
        for obj in cursor:
            res.append(obj)

        return res

    @property
    def db(self):
        return self.__db

    @property
    def name(self):
        return self.db.name


class DataReader:
    def __init__(self, read_dir, write_dir='./'):
        self.__readDir = read_dir
        self.__writeDir = write_dir

    def readFile(self, file_name, callback):
        if not self.fileExists(file_name):
            return False

        file_path = self.appendStringWithPath(self.readDir, file_name)
        file = open(file_path, 'r')
        i = 0
        for readLine in file:
            callback(readLine, i == 0, False)
            i += 1

        file.close()
        callback("", False, True)

    def fileExists(self, file_name):
        return os.path.exists(self.appendStringWithPath(self.readDir, file_name))

    def appendStringWithPath(self, s1, s2):
        return s1 + '/' + s2

    @property
    def readDir(self):
        return self.__readDir

    @readDir.setter
    def readDir(self, dr):
        self.__readDir = dr

    @property
    def writeDir(self):
        return self.__writeDir

    @writeDir.setter
    def writeDir(self, dr):
        self.__writeDir = dr


class SimpleDataImporter:
    def __init__(self, loggingEnable=False):
        self.__dbConnector = DBConnector(os.path.join(CONFIG_PATH, 'config.json'), )
        self.__dbConnector.connect()
        self.__db = self.__dbConnector.get_database_name('yelp', 'data')
        logging.basicConfig(filename=os.path.join(LOG_PATH, 'import.log'), level=logging.INFO, filemode='w')
        logging.info('Connected to MongoDB')

    def run(self, file_name, collection_name, cleanImport=False):
        pass
        dataReader = DataReader(DATASET_PATH)
        if dataReader.fileExists(file_name) and (self.__db != None):
            if cleanImport: self.__dbConnector.reset_database_name('yelp', collection_name)
            self.__db.openBulk()
            logging.info('Open bulk for inserting data')
            dataReader.readFile(file_name, self.readCallback)

    def readCallback(self, obj, isHeader, isFinished):
        if isFinished:
            self.__db.closeBulk()
            logging.info('Close bulk')
        else:
            self.__db.addToBulk(json.loads(obj))

    def finish(self):
        self.__dbConnector.disconnect()
        logging.info('Data has been imported.')

    @staticmethod
    def get_collection_name(dataset_name=None):
        if not dataset_name:
            return 'data'

        rep = {"yelp_academic_dataset_": "", ".json": ""}

        rep = dict((re.escape(k), v) for k, v in rep.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        collection_name = pattern.sub(lambda m: rep[re.escape(m.group(0))], dataset_name)

        return collection_name
