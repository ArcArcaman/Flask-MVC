from flask import render_template, request

def index():
    return render_template('root/index.html')
