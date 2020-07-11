import os
import sys
from flask import Flask, request, redirect, url_for,send_from_directory
from werkzeug import secure_filename
import uuid
import json
import conf
from task import sendFile
from md5 import GetFileMd5
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = conf.UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in conf.ALLOWED_EXTENSIONS

@app.route('/api/v1/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        task={}
        task["convertType"]=request.form.get('convertType')
        if not file:
        	return '{"msg": "请上传文件！"}'
        if not allowed_file(file.filename):
        	return '{"msg": "文件不允许！"}'
        else:
            if not task["convertType"]:
                task["convertType"]=conf.WPS
            filename = secure_filename(file.filename)
            task["id"]=str(uuid.uuid1())
            #task["id"]=str(GetFileMd5(file))
            
            path=app.config['UPLOAD_FOLDER']+'/'+task["id"]
            print(path)
            if os.path.isdir(path):
                task["status"]=conf.FINISHED
            else:
                task["status"]=conf.QUEUED
                os.makedirs(path)
                file.save(os.path.join(path, filename))
                sendFile.delay(task)
            return json.dumps(task,ensure_ascii=False)

@app.route('/api/v1/<task_id>', methods=['GET'])
def view_file(task_id):
	folder=app.config['UPLOAD_FOLDER']+'/'+task_id
	if not os.path.isdir(folder):
		return '{"msg": "id不正确！"}'
	task={}
	task["id"]=task_id
	print(folder+"/"+conf.FINISHED)
	print(os.path.exists(folder+"/"+conf.FINISHED))
	task["status"]=conf.FINISHED  if os.path.exists(folder+"/"+conf.FINISHED) else conf.QUEUED
	return json.dumps(task,ensure_ascii=False)
    




@app.route('/download/v1/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER']+'/'+filename,conf.PDF_NAME)

if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))