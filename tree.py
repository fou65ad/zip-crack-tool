import os
import zipfile,filetype
import time
import hashes
from fpdf import FPDF
import datetime

def type(item):
	kind = filetype.guess(item)
	res=''
   	if kind is None:
		res='Cannot guess file type!'
	else:
		res=kind.mime
   	return res


def browse(rootDir,g,dir=''):
	"""
	Browsing and printing the directory hierarchy , generating md5 and sha1 hashes for every file  
	in the root directory and subdirectories,generating pdf report
	"""
	
	if(rootDir==''):
		rootDir=os.getcwd()
	pdf = FPDF()
	pdf.add_page()
	format = "%a %b %d %H:%M:%S %Y"
	today = datetime.datetime.today()
	s = today.strftime(format)
	e=d= datetime.datetime.strptime(s, format)
	pdf.set_font('Arial', 'B', 22)
	pdf.cell(200, 10, 'LIST OF HASHES',align='C',ln=5)
	pdf.cell(125, 4, '',0,1,'C')
	pdf.set_font('Courier', '', 12)
	pdf.cell(115, 4, 'date  : '+str(d.strftime(format)),0,1)
	pdf.cell(125, 4, '',0,1,'C')
	pdf.cell(115, 4, 'root folder : " '+ rootDir+' "',0,1)
	pdf.cell(125, 4, '',0,1,'C')
	pdf.cell(115, 4, 'all files contained in this root folder and subfolders : ',0,1)
	pdf.cell(125, 4, '',0,1,'C')

	for dirName, subdirList, fileList in os.walk(rootDir):
		print('Found directory: %s' % dirName)

		for fname in fileList:
			print('\t%s' % fname)
			pdf.set_font('Times', 'I', 12)
			pdf.cell(40, 5, 'File : '+dirName+"/"+fname, ln=1)
			md5 = hashes.md5(dirName+"/"+fname)
			sha1 = hashes.sha1(dirName+"/"+fname)
			pdf.set_font('Courier', '', 10)
			pdf.cell(115, 4, 'MD5   : '+md5,0,1, 'C')
			pdf.cell(132, 4,  'SHA1  : '+sha1,0,1, 'C')
	res=''
	if(g==1):	
		if(dir==''):
			name='hashes_'+str(e).replace(' ','_')
			res = 'hashes_'+str(e).replace(' ','_')+'.pdf saved at the current directory'
		else:
			name=dir+'/'+'hashes_'+str(e).replace(' ','_')
			res = 'hashes_'+str(e).replace(' ','_')+'.pdf saved at '+name+'.pdf'
		pdf.output(name+'.pdf', 'F')	

		print res
	
def attack(zipfilename,dictionary,g,dir=''):
	"""
	Zipfile password cracker using a dictionary attack,generating pdf report
	"""

	pdf = FPDF()
	pdf.add_page()
	format = "%a %b %d %H:%M:%S %Y"
	today = datetime.datetime.today()
	s = today.strftime(format)
	e=d = datetime.datetime.strptime(s, format)
	sha1target= hashes.sha1(zipfilename)
	sha1wordlist= hashes.sha1(zipfilename)
	print '----------dictionary attack----------'
	print 'target   : '+zipfilename
	print 'wordlist : '+dictionary
	print 'started at :', d.strftime(format)
	start=datetime.datetime.now().replace(microsecond=0)
	pdf.set_font('Arial', 'B', 22)
	pdf.cell(200, 10, 'Attack Report',align='C',ln=5)
	pdf.set_font('Courier', '', 12)
	pdf.cell(125, 4, '',0,1,'C')
	pdf.cell(115, 4, 'target zip file  : " '+zipfilename+' "',0,1)
	pdf.set_font('Courier', '', 10)
	pdf.cell(125, 4, 'SHA1  : '+sha1target,0,1,'C')
	pdf.cell(125, 4, '',0,1,'C')
	pdf.set_font('Courier', '', 12)
	pdf.cell(115, 4, 'wordlist used  : " '+dictionary+' "',0,1)
	pdf.set_font('Courier', '', 10)
	pdf.cell(125, 4, 'SHA1  : '+sha1wordlist,0,1,'C')
	pdf.cell(125, 4, '',0,1,'C')
	pdf.set_font('Courier', '', 12)
	pdf.cell(115, 4, 'attack started at   : '+str(d.strftime(format)),0,1)
	password = None
	zip_file = zipfile.ZipFile(zipfilename)
	found=0
	attempts=0
	lis=zip_file.namelist()
	namedir=lis[0].split('/')[0]
	os.system('rm -r '+namedir)
	with open(dictionary, 'r') as f:
		for line in f.readlines():
			password = line.strip('\n')
			try:
				attempts+=1
				zip_file.extractall(pwd=password)
				print 'trying : "'+password +'"....accepted'
				print 'extracting ...'
				password = '[+] final result, password found : "%s"' % password
				found=1
				break
			except:
				print 'trying : "'+password +'"....wrong password'
				pass
	today = datetime.datetime.today()
	s = today.strftime(format)
	d = datetime.datetime.strptime(s, format)
	pdf.cell(125, 4, '',0,1,'C')
	pdf.cell(115, 4, 'attack finished at  : '+str(d.strftime(format)),0,1)
	print 'finished at :', d.strftime(format)
	end=datetime.datetime.now().replace(microsecond=0)
	pdf.cell(125, 4, '',0,1,'C')
	pdf.cell(115, 4, 'attack duration     : " '+str((end-start))+' "',0,1)
	pdf.cell(125, 4, '',0,1,'C')
	pdf.cell(115, 4, 'number of attempts  : '+str(attempts),0,1)
	pdf.cell(125, 4, '',0,1,'C')
	print 'number of attempts  : ',attempts
	print 'duration : ',(end-start)
	if (found):
		print password
		print 'target zipfile successfully extracted to : " '+namedir+' "'+' at the current working directory'
		pdf.cell(115, 4, password,0,1)
		pdf.cell(125, 4, '',0,1,'C')
		pdf.cell(115, 4, 'target zipfile successfully extracted to : " '+namedir+' "',0,1)
		pdf.cell(125, 4, '',0,1,'C')
		
	else :
		print "[-] final result : password not found"	
		pdf.cell(115, 4, "[-] final result : password not found",0,1)
		pdf.cell(125, 4, '',0,1,'C')
	

	if found:
		pdf.cell(115, 4, 'all files contained in this zip file with data type test : ',0,1)
		pdf.cell(125, 4, '',0,1,'C')
		lis=zip_file.namelist()
		for item in lis :
			if os.path.isfile(item):
		 		pdf.cell(40, 5, 'FILE : '+item, ln=1)
		 		pdf.cell(40, 5, 'MIME-TYPE : '+type(item), ln=1)
		 		pdf.cell(125, 4, '',0,1,'C')
	else:
		pdf.cell(115, 4, "can't perform data test on files ",0,1)
		pdf.cell(115, 4, "because  NO file was extracted (password not found)",0,1)

		pdf.cell(125, 4, '',0,1,'C')
	res=''
	if(g==1):
		if(dir==''):
			name='report_'+str(e).replace(' ','_')
			res = 'report_'+str(e).replace(' ','_')+'.pdf saved at the current directory'
		else:
			name=dir+'/'+'report_'+str(e).replace(' ','_')
			res = 'hashes_'+str(e).replace(' ','_')+'.pdf saved at '+name+'.pdf'
		pdf.output(name+'.pdf', 'F')	
		print res
	
#attack('eg.zip','wordlist.txt',1)

#browse('',1,'tes')