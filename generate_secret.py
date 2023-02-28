import random
import string
import base64
import hashlib

from decouple import config

code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

code_challenge = hashlib.sha256(code_verifier).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

import os
os.environ['CODE_VERIFIER'] = str(code_verifier)
print("code_verifier",config('CODE_VERIFIER'))
print("code_challenge",code_challenge)
client_id = config('ID')
print("client_id",client_id)
url = f'http://127.0.0.1:8000/o/authorize/?response_type=code&code_challenge={code_challenge}&code_challenge_method=S256&client_id={client_id}&redirect_uri=http://127.0.0.1:8000/noexist/callback'
print(url)

import requests

client = requests.Session()
res = client.get('http://localhost:8000/admin/')
client.headers['X-CSRFtoken']=res.cookies['csrftoken']

data={'username':'ares','password':'spiridon12','csrfmiddlewaretoken':res.cookies['csrftoken']}
resp = client.post('http://localhost:8000/admin/login/?next=/admin/',data = data,allow_redirects=True)
data={'csrfmiddlewaretoken':resp.cookies['csrftoken'],'x-csrftoken':resp.cookies['csrftoken']}
data.setdefault('SESSIONID',client.cookies['sessionid'])


client.headers['cookie'] = f"csrftoken={client.cookies['csrftoken']};sessionid={client.cookies['sessionid']}"
res = client.get(url,data=data,cookies=client.cookies,allow_redirects=True)

curl = f'curl -X POST \
    -H "Cache-Control: no-cache" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    "http://127.0.0.1:8000/o/token/" \
    -d "client_id=${config("ID")}" \
    -d "client_secret=${config("SECRET")}" \
    -d "code=${config("CODE")}" \
    -d "code_verifier=${config("CODE_VERIFIER")}" \
    -d "redirect_uri=http://127.0.0.1:8000/noexist/callback" \
    -d "grant_type=authorization_code"'

import subprocess
exec = subprocess.Popen(curl,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

print(exec.stdout.read())