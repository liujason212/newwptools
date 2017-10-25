from app import app
from app import sqlite_db
from flask import render_template, flash, redirect
from .forms import Web_config

@app.route('/config', methods = ['GET', 'POST'])

def config():
    form=Web_config()
    super_password=form.super_password.data
    if form.validate_on_submit() and super_password=='jasongo**':
        flash('提交成功')
        sqlite_db.initial_db()
        change_input=form.change_input.data
        change_type=form.change_type.data
        if len(change_input) !=0 and change_type=='token' :
            sqlite_db.update_db_token(change_input)
        if len(change_input) !=0 and change_type=='password' :
            sqlite_db.update_db_password(change_input)
    elif form.validate_on_submit() and super_password!='jasongo**':
        flash('密码错误')
    return render_template('config.html',form=form)

