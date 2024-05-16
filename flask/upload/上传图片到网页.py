import requests

import os

import re

url = r'http://127.0.0.1:5000/uploader/transmission'

#url = r'http://**.**.**.***:8080'

i = 1

for path, dirpath, file in os.walk(r"C:/flask/tpchulijieguo"):

    for f in file:

        r1 = r'(jpg)'

        if re.findall(r1, f):

            files = {'img': (f, open(r"C:/flask/tpchulijieguo/"+f, 'rb'), 'jpg', {})}

            print(files)

            res = requests.request("POST", url, data={"type": "1"}, files=files)

            i += 1

            print(res.text)
