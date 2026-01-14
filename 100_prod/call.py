import requests

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
    with open("automated_export.csv", "wb") as f:
        f.write(response.content)
    print("Download complete!")
else:
    print(f"Error: {response.status_code}")