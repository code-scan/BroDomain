#coding=utf-8
#author=cond0r@codescan
import threading
import Queue
from urllib import quote
import urllib2
import re
from time import sleep
import sys
class mthread(threading.Thread):
	def __init__(self,function,rfunction,args):
		threading.Thread.__init__(self)
		self.function=function
		self.args=args
		self.rfunction=rfunction
		self.SubDomain_regx='value="(.*)"><input type=hidden'		
	def run(self):
		while self.args.empty()==False:
			args=self.args.get(timeout=1)
			if args!=None:
				result=self.function(args)
				self.rfunction(result)
			else:
				break
		self.rfunction("Ennnnnnd") 

def GetSubByDomain(domain):
	url="http://i.links.cn/subdomain/?domain=%s&b2=1&b3=1&b4=1"%quote(domain)
	SubDomain_regx='value="(.*)"><input type=hidden'
	data=urllib2.urlopen(url).read()
	domain=re.findall(SubDomain_regx,data)
	return domain
result=Queue.Queue()

def process(function,rfunction,args,num):
	params=Queue.Queue()
	for a in args:
		params.put(a)
	for threads in xrange(num):
		mthread(function,rfunction,params).start()
def run(domain,prints):
	num=len(domain)/2
	if len(domain)>100:
		num=20		
	process(GetSubByDomain,prints,domain,num)		

