import sys
import os
import sqlite3

from DB_settings import SERVER_DB_PATH
conn = sqlite3.connect(SERVER_DB_PATH)

# def init_server_database():