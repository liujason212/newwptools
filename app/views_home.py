from app import  app
from flask import render_template,flash,redirect
from app import dnscheck,dkim_dmarc
from .forms import DnsCheck
@app.route('/',methods=['GET'])
@app.route("/index.html")
def index():
    return render_template('index.html')