import sys 
import requests

def login(name,pwd):
	url = 'http://1.1.1.2/ac_portal/login.php'
	payload = {
			'opr':'pwdLogin',
			'userName':name,
			'pwd': pwd,
			'rememberPwd':'1'
		   }
	r = requests.post(url, data = payload)
	if 'true' in r.text:
		sys.exit(1)
	elif 'false' in r.text:
		sys.exit(0)

	

def logout():
	url2 = 'http://1.1.1.2/ajaxlogout'
	r2 = requests.get(url2)

name = 'xxxxx'
pwd = 'xxxx'

if __name__ == '__main__':
	if sys.argv[1] == 'in':
		login(name,pwd)
	elif sys.argv[1] == 'out':
		logout()




