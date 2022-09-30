import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = 'username=benji87002@gmail.com&password=En6!xyVCbuXxuCX'

response = requests.post('https://opendata.nationalrail.co.uk/authenticate', headers=headers, data=data)
print(response)