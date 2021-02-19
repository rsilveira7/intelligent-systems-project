##################################### Automated Tests #######################################
import requests
import json
from datetime import datetime
now = datetime.now()
timestamp = datetime.timestamp(now)
import os

#variables
url = 'http://127.0.0.1:5000/v1/categorize'
headers = {'Content-Type': 'application/json'}
badrequest = "400 (Bad Request)"

print('##################################### Automated Tests #######################################\n')
print("Timestamp =", timestamp, '\n')

#Predictions OK
data = {"products":[{"query":"lembrancinhas de 15 anos","title":"lembrancinha 15 anos - lembrancinha de 15 anos","concatenated_tags":"15 anos"},{"query":"prateleira","title":"trio de nichos prateleira","concatenated_tags":"prateleiras decoracao gaveteiros nichos prateleiras nichos"},{"query":"lembrancinhas vingadores","title":"caixa meia bala vingadores","concatenated_tags":"vingadores super herois"}]}
x = requests.post(url, data=json.dumps(data), headers=headers)
print('Request Predictions - Test: ',x.text!=badrequest)

#Predictions OK by Json File
with open(os.environ['TEST_PRODUCTS_PATH']) as file_data:
    json_data = json.load(file_data)  
x = requests.post(url, data=json.dumps(json_data), headers=headers)
print('Predictions by Json File - Test: ',x.text!=badrequest)

#Bad request - missing key
data = {"products":[{"":"lembrancinhas de 15 anos","title":"lembrancinha 15 anos - lembrancinha de 15 anos","concatenated_tags":"15 anos"},{"query":"prateleira","title":"trio de nichos prateleira","concatenated_tags":"prateleiras decoracao gaveteiros nichos prateleiras nichos"},{"query":"lembrancinhas vingadores","title":"caixa meia bala vingadores","concatenated_tags":"vingadores super herois"}]}
x = requests.post(url, data=json.dumps(data), headers=headers)
print('Missing key - Test: ',x.text==badrequest)

#Bad request - missing header
{"products":[{"query":"lembrancinhas de 15 anos","title":"lembrancinha 15 anos - lembrancinha de 15 anos","concatenated_tags":"15 anos"},{"query":"prateleira","title":"trio de nichos prateleira","concatenated_tags":"prateleiras decoracao gaveteiros nichos prateleiras nichos"},{"query":"lembrancinhas vingadores","title":"caixa meia bala vingadores","concatenated_tags":"vingadores super herois"}]}
x = requests.post(url, data=json.dumps(data))
print('Missing Header - Test: ',x.text==badrequest)

#Bad request - bad structure
data = {"products":[{"":"lembrancinhas de 15 anos"}]}
x = requests.post(url, data=json.dumps(data), headers=headers)
print('Bad structure - Test: ',x.text==badrequest)
print('\n##################################### Automated Tests #######################################')
