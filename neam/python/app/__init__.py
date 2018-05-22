from flask import Flask

app = Flask(__name__)

from neam.python.app import routes

