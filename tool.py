#!/usr/bin/python
import sys, getopt,tree
def help():
   print 'usage : '
   print ''
   print 'SYNOPSIS :'
   print ''
   print 'python tool.py [OPTION]... '
   print ''
   print 'DESCRIPTION'
   print ''
   print 'with no options "python tool.py" will simply browse the current working directory and print its tree '
   print ''
   print 'OPTION :'
   print ''
   print '-F , --folder=<rootFolder>'
   print ''
   print '\tset the directory to browse eg. : -F /root/Desktop or --folder==/root/Desktop'
   print ''
   print '-e ,--export'
   print ''
   print '\tgenerates sha1 and md5 of every file in the current directory and its subdirectories'
   print '\tand exports the result in pdf format at the current working directory'
   print '\tif the attack was successful the target zipfile will be extracted the current directory'
   print '\tuse -F option to set the directory to browse'
   print '\tuse -o option to set the output directory of the generated pdf'
   print ''
   print '-z , --zipfile=<zipFile>'
   print ''
   print '\tset the target protected zip file to be attacked eg. : -z /root/target.zip or --zipfile==/root/target.zip '
   print ''
   print '-d, --dic=<wordlist>'
   print ''
   print '\tset the wordlist file to use in the attack eg. : -d /root/worldlist.txt or --dic==/root/worldlist.txt '
   print ''
   print '-r ,--report'
   print ''
   print '\tgenerate the report of the attack in pdf format at the current working directory'
   print '\tuse -o option to set the output directory of the generated pdf' 
   print ''
   print '-o,--out=<outputDirectory>'
   print ''
   print '\tset the output directory eg. : -o /root/Desktop/folder or --out =/root/Desktop/folder '
   print ''
   print '-s,--samples'
   print ''
   print '\tdisplays usage samples'
   print ''
   print '-h,--help'
   print ''
   print '\tfor help'
   print ''


def samples():
   print ''
   print 'EXAMPLES'
   print ''
   print 'python tool.py'
   print ''
   print '\tprints the tree of the current working directory'
   print ''
   print 'python tool.py -e'
   print ''
   print '\tprints the tree of the current working directory , generates sha1 and md5 of every file in the current directory and its subdirectories '
   print '\tand exports the result in the current working directory'
   print ''
   print 'python tool.py -eF /root/Desktop -o /root/Documents'
   print ''
   print '\tprints the tree of "/root/Desktop" directory , generates sha1 and md5 of every file in this directory and its subdirectories '
   print '\tand exports the result in "/root/Documents" directory'
   print ''
   print 'python tool.py -z eg.zip -d wordlist.txt'
   print ''
   print '\tattacks the protected zip file "eg.zip" using wordlist "wordlist.txt" '
   print ''
   print 'python tool.py -rz eg.zip -d wordlist.txt'
   print ''
   print '\tattacks the protected zip file "eg.zip" using wordlist "wordlist.txt" and generates the report '
   print '\tof the attack at the current working directory'
   print ''
   print 'python tool.py -rz eg.zip -d wordlist.txt -o /root/Documents'
   print ''
   print '\tattacks the protected zip file "eg.zip" using wordlist "wordlist.txt" and generates the report '
   print '\tof the attack at the "/root/Documents" directory'
   print ''
   print 'NOTE'
   print ''
   print '\targuments parsing supports the conventions established by the Unix function getopt()'
   print '\tmeans for example that the following commands are the same : '
   print ''
   print '\tpython tool.py -eF /root/Desktop -o /root/Documents'
   print '\tpython tool.py -o /root/Documents -e -F /root/Desktop '
   print '\tpython tool.py --out=/root/Documents --folder=older/root/Desktop --export '
   print ''
   print '\tso you are free to combine options with the order you want , like a unix command'



def main(argv):
   r=e=0
   out=zipfile=folder=dic=''
  
   try:
      opts, args = getopt.getopt(argv,"hz:o:F:d:ers",["zipfile=","out=","root=","dic=","export","report","samples","help"])
   except getopt.GetoptError:
      print 'command not found, use : -h , --help for help '
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h", "--help"):
         help()
         sys.exit()
      if opt in ("-s", "--samples"):
         samples()
         sys.exit()
      elif opt in ("-z", "--zipfile"):
         zipfile = arg
      elif opt in ("-o", "--out"):
         out = arg
      elif opt in ("-d", "--dic"):
         dic = arg
      elif opt in ("-F", "--folder"):
         folder = arg
      elif opt in ("-r", "--report"):
         r = 1
      elif opt in ("-e", "--export"):
         e = 1
   if(zipfile!=''):
      if(dic!=''):
         tree.attack(zipfile,dic,r,out)
      else:
         print 'you should specify the worldlist : -d FILE or --dic FILE'
   else:
      tree.browse(folder,e,out)

if __name__ == '__main__':
   main(sys.argv[1:])
