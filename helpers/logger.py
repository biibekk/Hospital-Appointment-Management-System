import logging

logging.basicConfig(format='%(asctime)s %(name)s %(levelname) -8s [%(filename) s:%(lineno)d] %(message)s',
                    level=logging.DEBUG,
                    filename="logs/database.log",
                    datefmt="%d-%m—%Y %H:%M:%S")
dblogger = logging.getLogger("Database")

