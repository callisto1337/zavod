import xml.etree.ElementTree as ET
import requests

root = ET.parse('sitemap.xml').getroot()
counter, successes, errors = 0, 0, 0
urls = []

while counter < len(root):
    urls.append(root[counter][0].text)
    counter += 1
counter = 0

for n in urls:
    counter += 1
    r = requests.get(n)
    if r.status_code != 200:
        print(r.status_code)
        errors += 1
    if r.status_code == 200:
        print('Success: ',  counter)
        successes += 1

print('All url: ', len(urls))
print('Errors: ', errors)
print('Successes: ', successes)

