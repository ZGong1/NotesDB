from flask import *
import os
import time

app = Flask(__name__)

#loads db on the main page
@app.route('/')
def initial_redirect():
	return note_list()

@app.route('/change/<file>', methods = ['POST', 'GET'])
def change_file(file):
	if session['secret'] == 'ZGong':
		new = request.form['new']
		os.system(f"mv /root/Flask/templates/notes/\"{file}\" /root/Flask/templates/backups")
		with open(f"/root/Flask/templates/notes/{file}", 'w') as f:
			f.write(new)
	return redirect('/')

@app.route('/edit/<file>')
def edit_file(file):
	if session['secret'] == 'ZGong':
		with open(f"/root/Flask/templates/notes/{file}", 'r') as f:
			old = f.read()
		return render_template('edit.html', file = file, old = old)
	return redirect('/')

@app.route('/addpage')
def add_page():
	if session['secret'] == 'Secret code':
		return render_template('index.html')
	return redirect('/')

@app.route('/addnotes', methods = ['POST', 'GET'])
def add_notes():
	if session['secret'] == 'Secret code':
		notes = request.form['notes']
		date = time.strftime("%m-%d-%Y-%H-%M-%S")
		subject = request.form['subject']
		with open(f"./templates/notes/{subject}:{date}.txt", "a") as f:
			f.write(notes)
		return initial_redirect()
	return redirect('/')

@app.route('/note_list')
def note_list():
	filelist = []
	for file in os.listdir('./templates/notes'):
		filelist.append(file)
	filelist.sort()
	return render_template('list.html', files = filelist)

@app.route('/open/<file>')
def open_file(file):
	files = []
	files.append(file)
	return render_template('subject.html', files = files)

@app.route('/subject', methods = ['POST', 'GET'])
def open_class():
	files = []
	subject = request.form['subject']
	for file in os.listdir('./templates/notes'):
		if subject in file:
			files.append(file)
	files.sort()
	return render_template('subject.html', files = files)

@app.route('/addsecret', methods = ['POST', 'GET'])
def add_secret():
	secret = request.form['secret']
	session['secret'] = secret
	return redirect('/')

#sets up the flask app
if __name__ == '__main__':
#insert secret key to keep the session safe    app.config['SECRET_KEY'] = ''
    app.run(host="0.0.0.0", port=25110)
