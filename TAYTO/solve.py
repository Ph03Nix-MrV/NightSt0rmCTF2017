from string import *
from pyfiglet import *
from pwn import *

s=digits+ascii_uppercase
f=Figlet(font='jerusalem')

def check(i,s):
  if (s[0][i]==' ') and (s[1][i]==' ') and (s[2][i]==' ') and (s[3][i]==' ') and (s[4][i]==' '):
    return True
  return False

def splitfiglet(tmp_s,rs):
  prev = 0
  for k in range(len(tmp_s[0])):
    if check(k,tmp_s)==False:
      continue
    if len(tmp_s[0][prev:k])>0:
      rs.append(tmp_s[0][prev:k])
      rs.append(tmp_s[1][prev:k])
      rs.append(tmp_s[2][prev:k])
      rs.append(tmp_s[3][prev:k])
      rs.append(tmp_s[4][prev:k])
    prev = k+1
  return rs

def creatdict(value,rs):
  j=0
  for i in s:
    tmp = ''.join(rs[j:j+5])
    value[i]=tmp
    j+=5
  return value

def clearrs(txt):
  txt = txt.split('\n')
  a=[]
  for i in range(len(txt)):
    txt[i] = txt[i].lstrip()
    a.append(len(txt[i]))
  for i in range(len(txt)):
    if len(txt[i]) < max(a):
      txt[i] = ' '*(max(a) - len(txt[i])) + txt[i]
  a=[]
  for i in range(len(txt)):
    txt[i] = txt[i].rstrip()
    a.append(len(txt[i]))
  for i in range(len(txt)):
    if len(txt[i]) <= max(a):
      txt[i] += ' '*(max(a) - len(txt[i]) + 1)
  return list(txt)

def getque(que,rs):
  for i in range(0,len(rs),5):
    que.append(''.join(rs[i:i+5]))
  return que

rs=[]
value={}
for i in range(0,len(s),8):
  tmp =''.join([i+' ' for i in s[i:i+8]])
  tmp_s = f.renderText(tmp[::-1])
  tmp_s = clearrs(tmp_s)[1:]
  rs = splitfiglet(tmp_s,rs)
value =creatdict(value,rs)
r=remote('103.69.195.108',8888)
while True:
  res =r.recv()
  print res
  if 'NightSt0rm' in res:
    break
  res=r.recv()
  print res
  res = clearrs(res)
  que_rs=[]
  que_rs = splitfiglet(res,que_rs)
  que=[]
  que =getque(que,que_rs)
  send=''
  for i in que:
    for key, val in value.iteritems():
      if val == i:
        send+=key
        break
  r.sendline(send)

