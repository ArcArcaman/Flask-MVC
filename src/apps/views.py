from flask import render_template, request, session, redirect, url_for

def app():
    return render_template('apps/apps.html')
