# Command level request library
from bs4 import BeautifulSoup
import requests
import json

domainName = 'https://p-bandai.com/hk/'
CSRFToken = ''

# Account Informaiton
accName = ''
accPW = ''

# Item Information
itemCode = ''
qty = 1

fileName = ''
try:
	f = open('./config.txt', 'r')
	accName = f.readline().replace('\n', '').split('=')[1]
	accPW = f.readline().replace('\n', '').split('=')[1]
	itemCode = f.readline().replace('\n', '').split('=')[1]
	qty = int(f.readline().replace('\n', '').split('=')[1])
except IOError as exc:
	print('Config file not found')
	sys.exit(exc.errno)

print('Account Name : ' + accName)
print('Account Password : ' + accPW)
print('Item Code : ' + itemCode)
print('Item qty : ' + str(qty))

session = requests.Session()
r = session.get(domainName + 'login/')
soup = BeautifulSoup(r.content, 'lxml')
pb_tracking_id = ''
for div in soup.find_all('input', attrs={'name': 'CSRFToken'}):
    CSRFToken = div['value']
for div in soup.find_all('input', attrs={'name': 'pb_tracking_id'}):
    pb_tracking_id = div['value']

payload = { 'j_username': accName, 
            'j_password': accPW,
            'CSRFToken': CSRFToken,
            'pb_tracking_id': pb_tracking_id }
r = session.post(domainName + 'login/', data = payload)
soup = BeautifulSoup(r.content, 'lxml')
print('Log in')
soup = BeautifulSoup(r.content, 'lxml')
if soup.find('span',attrs={'id':'PBLoginForm.errors'}):
	print('Login error')
	sys.exit()
print('Login success')

#Ordering
payload = {'productCodePost': itemCode,
			'qty': qty,
			'CSRFToken':CSRFToken}
addLooping = True

#loop here
while addLooping:
	pass
	r = session.post(domainName + 'cart/add/', data = payload)
	soup = BeautifulSoup(r.content, 'lxml')
	site_json=json.loads(soup.text)
	if r.status_code == 200:
		print('Adding')
		if len(site_json['cartAnalyticsData']['cartCode']) > 0:
			print('Item Added')
			addLooping = False



confirmLooping = True
while confirmLooping:
	r = session.get(domainName + 'checkout/orderinformation')
	if r.status_code == 200:
		confirmLooping = False
print('Order Information confirm')

soup = BeautifulSoup(r.content, 'lxml')
shippingAddId = ''
cartEncryptedPk = ''
for div in soup.find_all('input', attrs={'name': 'shippingAddId'}):
	shippingAddId = div['value']
for div in soup.find_all('input', attrs={'name': 'cartEncryptedPk'}):
	cartEncryptedPk = div['value']

#Payment Method
print('Address confirm')

# if not soup.find('input',attrs={'id':'radio-1'}).has_attr('checked'):
print('Payment method confirm')
payload  = {'orderConfirmationUrl':'/hk/checkout/orderinformation/submit',
			'shippingAddId':shippingAddId,
			'cartEncryptedPk':cartEncryptedPk,
			'shippingCountryCode':'HK',
			'justReload':'true',
			'paymentMethodId':'paypal',
			'voucherCode':'',
			'CSRFToken':CSRFToken}
r = session.post(domainName + 'checkout/orderinformation/submit/setPaymentMethod', data =payload)
r = session.get(domainName + 'checkout/orderinformation/')
r = session.post(domainName + 'checkout/orderinformation/submit/', data =payload)
r = session.get(domainName + 'checkout/confirm')
# else :
# 	print('Paymen method find')
	# r = session.get(domainName + 'checkout/confirm')

r = session.get(domainName + 'checkout/orderinformation')
soup = BeautifulSoup(r.content, 'lxml')
for div in soup.find_all('input', attrs={'name': 'cartEncryptedPk'}):
	cartEncryptedPk = div['value']


print('Payment confirm')

payload = {'cartEncryptedPk':cartEncryptedPk,
			'agree': 'True',
			'CSRFToken':CSRFToken}
r = session.post(domainName + 'checkout/confirm/placeorder', data = payload)
soup = BeautifulSoup(r.content, 'lxml')



#Paypal Method
paypalLogin = ''
paypalPass = ''
paypalAmt = ''
paypalTxnid = ''
paypalTxncurr = ''
paypalOd = ''
paypalSignature = ''
paypalRu = ''
paypalCallbackUrl = ''
paypalPaymentMethod = ''
paypalLang = ''
paypalUdf1 = ''
paypalUdf2 = ''
paypalCSRFToken = ''

for div in soup.find_all('form', attrs={'id': 'sdpRequestForm'}):
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Login'}):
    	paypalLogin	= divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Pass'}):
    	paypalPass = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Amt'}):
    	paypalAmt = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Txnid'}):
    	paypalTxnid = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_txncurr'}):
    	paypalTxncurr = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Od'}):
    	paypalOd = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Signature'}):
    	paypalSignature = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Ru'}):
    	paypalRu = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_CallbackUrl'}):
    	paypalCallbackUrl = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_PaymentMethod'}):
    	paypalPaymentMethod = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Lang'}):
    	paypalLang = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Udf1'}):
    	paypalUdf1 = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'SC_O01_04_Udf2'}):
    	paypalUdf2 = divSub['value']
    for divSub in div.find_all('input', attrs={'id': 'CSRFToken'}):
    	paypalCSRFToken = divSub['value']

print('Item = '+paypalOd)
print('PayPal $ '+paypalAmt)

paypalLooping = True

while paypalLooping:
	payload = {
				'login':paypalLogin,
				'pass':paypalPass,
				'amt':paypalAmt,
				'txnid':paypalTxnid,
				'txncurr':paypalTxncurr,
				'od':paypalOd,
				'signature':paypalSignature,
				'ru':paypalRu,
				'callbackUrl':paypalCallbackUrl,
				'paymentMethod':paypalPaymentMethod,
				'lang':paypalLang,
				'udf1':paypalUdf1,
				'udf2':paypalUdf2,
				'CSRFToken':paypalCSRFToken
			}
	r = session.post('https://prod.ndhkpay.com/Ndhk_Api/paymentRequest', data = payload)

	soup = BeautifulSoup(r.content, 'lxml')

	paypalToken = ''
	for div in soup.find_all('form', attrs={'id': 'redirectForm'}):
	    for divSub in div.find_all('input', attrs={'name': 'token'}):
	    	paypalToken	= divSub['value']

	print('Paypal popups')
	print('https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token='+paypalToken)

	if paypalToken != '':
		paypalLooping = False









