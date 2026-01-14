import requests
import re

url = "http://127.0.0.1:5000/export"
payload = {
    "category": "Business",
    #"category": "User",
    #"sub_category": "Reviews",
    #"sub_category": "Account Info",
    "search_term": "Artisan"
}

response = requests.post(url, data=payload)

if response.status_code == 200:
    # Get filename from the Content-Disposition header
    d = response.headers.get('content-disposition')
    fname = re.findall("filename=(.+)", d)[0]
    
    with open(fname, "wb") as f:
        f.write(response.content)
    print(f"Saved as: {fname}")
else:
    print(f"Error: {response.status_code}")