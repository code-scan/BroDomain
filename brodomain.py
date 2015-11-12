#coding=utf-8
#author=cond0r
import urllib2
import re
from urllib import unquote
from urllib import quote
from binascii import b2a_base64 as base64_encode
from binascii import a2b_base64 as base64_decode
from sys import argv
class aizhan:
	def __init__(self,domain='',mail='',name=''):
		self.domain=domain
		self.mail=mail
		self.name=name
		self.GetMailByDomain_regx='<a href="/reverse-whois\?q=(.*)&t=emailCode">'
		self.GetSameDomainByEmailCode_mail='onClick="DisplayAllSitesBox\(\);" value="(.*)" />'
		self.GetSameDomainByEmailCode_domain='<a target="_blank" class="links" rel="nofollow" href="(.*)">'
		self.GetRegname_regx='<a href="/reverse-whois\?q=(.*)&t=registrant">'
		self.GetRegname_List='<a href="/reverse-whois\?q=(.*)&t=registrant">'
		self.SameDomain=[]
		self.RegEmail=''
		self.RegName=''
		self.RegName_List=[]
		self.BroDomain=[]
	def AppendDomain(self,Dlist):
		for D in Dlist:
			self.SameDomain.append(D)
	def AppendBro(self,Dlist):
		for D in Dlist:
			if D not in self.BroDomain:
				#print D
				self.BroDomain.append(D)
	def AppendRegName(self,Rlist):
		for R in Rlist:
			if R not in self.RegName_List:
				self.RegName_List.append(R)
	def GetDomainFromReglist(self):
		Domain=[]
		i=1;
		for N in self.RegName_List:
			print i,
			i+=1
			dom=self.GetSameDomainByEmailCode(N,3,True)
			self.AppendBro(dom)

		#return Domain
	
	def GetSameDomainByEmailCode(self,emailcode,code=1,appends=False):
		if code==1:
			url="http://whois.aizhan.com/reverse-whois?q=%s&t=emailCode"%quote(emailcode)
		elif code==2:
			url="http://whois.aizhan.com/reverse-whois?q=%s&t=email"%quote(emailcode)
		elif code==3:
			url="http://whois.aizhan.com/reverse-whois?q=%s&t=registrant"%quote(emailcode)
		#print url
		data=urllib2.urlopen(url).read()
		email=re.findall(self.GetSameDomainByEmailCode_mail,data)
		if len(email)==1:
			email=email[0]
		else:
			email=''
		domain=re.findall(self.GetSameDomainByEmailCode_domain,data)
		if len(domain)==0:
			domain=''
		if appends:
			return domain
		self.AppendDomain(domain)
		if code==2 or code==1:			
			self.RegEmail=email		
		regname_list=re.findall(self.GetRegname_List,data)
		self.AppendRegName(regname_list)
		
	def GetMailByDomain(self):
		url="http://whois.aizhan.com/reverse-whois?q=%s&t=domain"%self.domain
		data=urllib2.urlopen(url).read()
		reg=re.findall(self.GetMailByDomain_regx,data)
		if len(reg)==1:		
			reg=unquote(reg[0])
			self.GetSameDomainByEmailCode(reg)
		reg_name=re.findall(self.GetRegname_regx,data)
		if len(reg_name)==1:
			self.RegName=reg_name[0]
			self.GetSameDomainByEmailCode(self.RegName,3)
			

if len(argv)!=2:
	print "Usage: python brodomain.py codescan.cn"
	exit()
print "[*] Init.."
query=aizhan(argv[1])
print "[*] Query Email.."
query.GetMailByDomain()
print "[*] Query All Domain Waiting.."
print "[*] Query ",
query.GetDomainFromReglist()
data="Email: %s\nRegistrant: %s\n"%(query.RegEmail,query.RegName)
data+="BroDmain Count:%d\n"%len(query.BroDomain)
for D in query.BroDomain:
	data+=D+"\n"
open('%s.log'%argv[1],'w').write(data)
print data
