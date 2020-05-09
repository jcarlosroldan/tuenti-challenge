from requests import get

URL = "https://52.49.91.111:8443/ghost"

headers = {"Range": "bytes=4017-8120"}

r = get(URL, verify = False, headers = headers)

print(r.text)
print(len(r.text))
print(r.headers)

# after discovering this, I set SSL decryption on Wireshark and sent it again :)