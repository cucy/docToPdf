import os
REDIS_URL='redis://192.168.223.16:6379/0'
UPLOAD_FOLDER = os.path.abspath('../uploads')
FINISHED='finished'
QUEUED='queued'
PDF_NAME="pdf.pdf"
ALLOWED_EXTENSIONS = set(['docx', 'doc', 'ppt', 'pptx', 'xls', 'xlsx'])
WORD = set(['docx', 'doc'])
PPT = set(['ppt', 'pptx'])
EXCEL = set(['xls', 'xlsx'])
OFFICE='office'
WPS='wps'