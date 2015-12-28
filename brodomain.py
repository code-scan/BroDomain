#coding=utf-8
#author=cond0r
import urllib2
import re
from urllib import unquote
from urllib import quote
from binascii import b2a_base64 as base64_encode
from binascii import a2b_base64 as base64_decode
from sys import argv
from Queue import Queue
import sys
import lib.mthread
class aizhan:
	def __init__(self,domain='',mail='',name=''):
		self.domain=domain
		self.domain_beian=domain
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
	def GetDomainBybeian(self,domain='',backquery=False):
		if domain:
			self.domain_beian=domain
		url='http://codescan.cn/beian.php?query=%s'%self.domain_beian
		data=urllib2.urlopen(url).read()
		r=re.findall('<td>([\s\S]*?)</td>',data)
		#print r
		dlist=[]
		for i in r:

			i=i.replace('	','').replace('\n','').replace('\r','')
			if 'ICP' in i and backquery==False:
				beian=i
				if '-' in beian:
					beian=beian.split('-')[0]
				self.GetDomainBybeian(beian,True)
				break
			if '.' in i :
				dlist.append(i)
				#print i
		self.AppendBro(dlist)


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
		#print url
		data=urllib2.urlopen(url).read()
		reg=re.findall(self.GetMailByDomain_regx,data)
		if len(reg)==1:
			reg=unquote(reg[0])
			self.GetSameDomainByEmailCode(reg)
		reg_name=re.findall(self.GetRegname_regx,data)
		if len(reg_name)==1:
			self.RegName=reg_name[0]
			self.GetSameDomainByEmailCode(self.RegName,3)
result=[]
def stdout( name):
	global result
	scanow ='[*] Find %s of %d'%(name,len(result))
	sys.stdout.write(str(scanow)+" "*20+"\b\b\r")
	sys.stdout.flush()
def prints(d):
	global result,data,over
	if d=='Ennnnnnd':
		if over==1:
			return 0
		over=1
		data+="SubDomain\n"
		for p in result:
			if p:
				p=p.replace("http://","").replace("https://","").replace("/","")
				data+=p+"\n"
		print "[*] Query Over,Result is in %s.log"	%argv[1]
		open('./log/%s.log'%argv[1],'w').write(data)
		return 1
	for i in d:
		stdout(i)
		result.append(i)
result_ip=[]
def prints_ip(d):
	global result_ip,data,over
	if 'Ennnn' not in d:
		result_ip.append(d)


def write_html(dicts):
	html=""
	for key,value in dicts.items():
		#print key,value
		if value!='':
			data='''		<li>
				<div class="link"><i class="fa fa-paint-brush"></i>{Domain}<i class="fa fa-chevron-down"></i></div>
				<ul class="submenu">
					{li}
			</ul>
			</li>
			'''.replace("{Domain}",key)
			li=""

			for d in value.split(","):
				if d:
					li+='<li><a href="'+d+'">'+d+'</a></li>'
			data=data.replace("{li}",li)
			html+=data

	htmls=open('./log/result.template').read()
	htmls=htmls.replace("{html}",html)
	open('./log/'+argv[1]+".html",'w').write(htmls)
over=0
if len(argv)!=2:
	print "Usage: python brodomain.py codevscan.cn"
	exit()
print "[*] Init.."
query=aizhan(argv[1])
print "[*] Query Email.."
query.GetMailByDomain()
print "[*] Query Beian Code.."
query.GetDomainBybeian()
print "[*] Query All Domain Waiting.."
print "[*] Query ",
query.GetDomainFromReglist()
data="Email: %s\nRegistrant: %s\n"%(query.RegEmail,query.RegName)
data+="BroDmain Count:%d\n"%len(query.BroDomain)
print "\n[*] BroDmain Count:%d\n"%len(query.BroDomain)
for D in query.BroDomain:
	D=D.replace("http://","").replace("https://","").replace("/","")
	data+=D+"\n"
m=lib.mthread.run(query.BroDomain,prints)
m=lib.mthread.runip(result,prints_ip)
dicts={}
for Ds in query.BroDomain:
	Ds=Ds.replace("http://www",'')
	Ds=Ds.replace("/",'')
	#print Ds
	dicts.update({Ds:''})
	for D in result:
		#print D
		if Ds in D:
			#print D
			data=dicts[Ds]
			dicts.update({Ds:data+","+D})
print "[*] Html Result in "+argv[1]+".html"
write_html(dicts)
