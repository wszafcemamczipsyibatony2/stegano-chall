import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from binascii import hexlify
from base64 import b64decode, b64encode
flag = open("flag.txt", "r").readline().strip()

def isSafe(input):
	blacklist = ["flag.txt", "flag", "cat", ">", "<", "''", "$ifs", "..", "/", "\\", "tail"]
	for i in blacklist:
		if i in input:
			return False
	return True

UPLOAD_FOLDER = 'temp'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.add_url_rule(
	"/temp/<name>", endpoint="check_exif_tool", build_only=True
)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# If the user does not select a file, the browser submits an
		# empty file without a filename.
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file:
			fname = file.filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
			if not "encoded" in request.form:
				fname = b64encode(fname.encode('utf-8')).decode()
			return redirect(url_for('check_exif_tool', name=fname))
	return '''
	<!doctype html>
	<title>Stegano solver!</title>
	<h1>Stegano solver!</h1>
	<form method=post enctype=multipart/form-data>
	  <p>Do you want to encode your filename?
		<input type=checkbox name=encoded>
	  </p>
	  <input type=file name=file>
	  <input type=submit value=Upload>
	</form>
	<h3>Checkout this awesome example how you can find flags in stegano challs!</h3>
	<a href="/temp/bG9nby5wbmc=">Click!</a>
	'''

@app.route('/temp/<name>')
def check_exif_tool(name):
	try:
		name = b64decode(name).decode()
	except:
		return """
			<h1>This is not base64 name!!!!!</h1>
		"""
	stream = os.popen(f'exiftool ./temp/{name}')
	output = stream.readlines()
	if len(output) == 0 or not isSafe(name):
		return '''
		<!doctype html>
		<title>404!</title>
		<h1>404</h1>
		<p>Not on my watch!</p>
		'''
	html = f'''
	<!doctype html>
	<title>Viewing : "{name}"</title>
	<h2>Stegano solver!</h2>
	<ul>
	'''
	for line in output:
		html += f"<li>{line}</li>\n"
	html += "</ul>"
	html += '<a href="/">Home</a>'
	return html
