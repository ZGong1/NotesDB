from flask import *
import sqlite3 as sql
import os
import time

app = Flask(__name__)

#loads db on the main page
@app.route('/')
def initial_redirect():
	return render_template('index.html')


@app.route('/addnotes', methods = ['POST', 'GET'])
def add_notes():
	notes = request.form['notes']
	date = time.strftime("%m-%d-%Y")
	subject = request.form['subject']
	with open(f"./templates/notes/{subject}:{date}.txt", "w") as f:
		f.write(notes)
	return initial_redirect()

@app.route('/note_list')
def note_list():
	filelist = []
	for file in os.listdir('./templates/notes'):
		filelist.append(file)
	return render_template('list.html', files = filelist)

#update with its own template and not just spit out a return
@app.route('/open/<file>')
def open_file(file):
	with open(f"./templates/notes/{file}", 'a') as f:
		return f"<div style='white-space: pre-wrap;'>{f.read()}</div>"

@app.route('/subject', methods = ['POST', 'GET'])
def open_class():
	files = []
	subject = request.form['subject']
	for file in os.listdir('./templates/notes'):
		if subject in file:
			files.append(file)
	return render_template('subject.html', files = files)

#sets up the flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=25110)
