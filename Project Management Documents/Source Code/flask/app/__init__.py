from flask import Flask
from config import Config  # from config.py import class Config

# application object as an instance of class Flask imported from the flask package
app = Flask(__name__)
app.jinja_options["line_comment_prefix"] = "#"
app.config.from_object(Config)

from app import routes
