# ex:set ts=2:

from subprocess import Popen, PIPE, STDOUT

def system (command):
  p = Popen(command, shell=True)
  p.communicate()

def system_reply (command):
  p = Popen(command, shell=True, stdout=PIPE, close_fds=True)
  return p.stdout.readlines()

def readfile (filename):
  fo = open(filename)
  lines = fo.readlines()
  fo.close()
  return lines

def writefile (filename, contents):
  fo = open(filename, 'w')
  fo.writelines(contents)
  fo.close()

