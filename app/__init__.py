import os

from flask import Flask
app = Flask(__name__)
app.config.from_object('config')
from app import views,views_zoho,views_home,views_webconfig

