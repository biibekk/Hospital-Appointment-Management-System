import sqlite3

class DatabaseConnection:
    _instance = None

    _initialized=False

    def __new__(cls,*args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,host):
        if self._initialized:
            return
        self.connection=sqlite3.connect(host)
        self._initialized=True
