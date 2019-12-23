from flask import render_template, request, session, redirect, url_for, jsonify
import database.connections as dbconn

def api():
    cur = dbconn.connection_all['TestDB'].getCursor()

    cur.execute("SELECT * FROM User")

    result = cur.fetchall()

    return jsonify(list(map(list, result)))
    
