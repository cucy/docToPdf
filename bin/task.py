import sys
import os
import comtypes.client
import win32com.client
import time
import conf
from celery import Celery

celery = Celery('tasks', broker=conf.REDIS_URL)

@celery.task
def sendFile(task):
	in_path=conf.UPLOAD_FOLDER+"/"+task['id']+"/"
	filename=os.listdir(in_path)[0]
	in_file = os.path.abspath(in_path+filename)
	out_file = os.path.abspath(in_path+conf.PDF_NAME)
	print(task['id']+'begin convert')
	if('.' in filename and filename.rsplit('.', 1)[1] in conf.WORD):
		word2pdf(in_file,out_file,task)
	elif('.' in filename and filename.rsplit('.', 1)[1] in conf.PPT):
		ppt2pdf(in_file,out_file,task)
	elif('.' in filename and filename.rsplit('.', 1)[1] in conf.EXCEL):
		excel2pdf(in_file,out_file,task)
	os.makedirs(in_path+conf.FINISHED)
	print(task['id']+'convert finished')
	time.sleep(2.0)

def ppt2pdf(in_file,out_file,task):
	if(task['convertType']==conf.OFFICE):
		wdFormatPDF = 32
		word = comtypes.client.CreateObject("Powerpoint.Application")
		doc = word.Presentations.Open(in_file,False,False,False)
		doc.SaveAs(out_file, FileFormat=wdFormatPDF)
		doc.Close()
		word.Quit()
	else:
		wpp = win32com.client.Dispatch("Kwpp.Application")
		ppt = wpp.Presentations.Open(in_file)
		ppt.SaveAs(out_file,32)
		ppt.Close()
		wpp.Quit()

def word2pdf(in_file,out_file,task):
	if(task['convertType']==conf.OFFICE):
		wdFormatPDF = 17
		word = comtypes.client.CreateObject('Word.Application')
		doc = word.Documents.Open(in_file)
		doc.SaveAs(out_file, FileFormat=wdFormatPDF)
		doc.Close()
		word.Quit()
	else:
		#stat = os.system('taskkill /im wps.exe')
		o = win32com.client.Dispatch("Kwps.Application")
		o.Visible=False
		doc = o.Documents.Open(in_file);
		doc.ExportAsFixedFormat(out_file,17)
		doc.Close()
		o.Quit();

def excel2pdf(in_file,out_file,task):
	if(task['convertType']==conf.OFFICE):
		word = comtypes.client.CreateObject('Excel.Application')
		doc = word.Workbooks.Open(in_file)
		doc.ExportAsFixedFormat(0,out_file,1,0)
		doc.Close()
		word.Quit()
	else:
		o = win32com.client.Dispatch("KET.Application")
		o.Visible=False
		doc = o.Workbooks.Open(in_file);
		doc.ExportAsFixedFormat(0,out_file,1,0)
		doc.Close()
		o.Quit();








def ppt2pdftest(input, output):
  p = win32com.client.Dispatch("PowerPoint.Application")
  p.Visible=1
  try:
    ppt = p.Presentations.Open(input, False, False, False)
	
    ppt.ExportAsFixedFormat(output, 2, PrintRange=None)
    return 0
  except:
    return 1
  finally:
    p.Quit()


if __name__ == "__main__":
	ppt2pdftest("""C:\\Users\\zrd\\Desktop\\1.pptx""", """C:\\Users\\zrd\\Desktop\\tmp\\22.pdf""")
