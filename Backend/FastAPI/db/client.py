### MongoDB client ###

# Descarga version comunity: https://www.mongodb.com/try/download
# Instalacion: instalar los MSI que descargues
# Modulo conexion MongoDB: pip install pymongo
# Ejecucion: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# conexion: mongodb://localhost
# descargar la extesion mongodb en VSC


from pymongo import MongoClient

db_client = MongoClient().local

