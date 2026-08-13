import logging

# logging.basicConfig(format='%(asctime)s %(name)s %(levelname) -8s [%(filename) s:%(lineno)d] %(message)s',
#                     level=logging.DEBUG,
#                     filename="logs/Hospital.log",
#                     datefmt="%d-%m—%Y %H:%M:%S")
# dblogger = logging.getLogger("Database")

# dblogger.debug("demo")

dbformatter = logging.Formatter('%(asctime)s %(name)s %(levelname) -8s [%(filename) s:%(lineno)d %(message)s]',datefmt="%d-%m-%Y %H:%M:%S")

dblogger = logging.getLogger('Database')
dblogger.setLevel(logging.DEBUG)
dblogger.propagate = False


db_fh = logging.FileHandler("logs/database.log")
db_fh.setLevel(logging.DEBUG)
db_fh.setFormatter(dbformatter)

if not dblogger.handlers:
    dblogger.addHandler(db_fh)

