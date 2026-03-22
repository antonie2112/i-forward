import json
import os

new_data = [
  {"code": "7106044", "name": "Lime Away", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH102104000.png"},
  {"code": "7106043", "name": "Greasecutter", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH102102500.png"},
  {"code": "7106045", "name": "Mikro Quat", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH102104520.png"},
  {"code": "7306280", "name": "Topax 66", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/VN7305178.png"},
  {"code": "7101070", "name": "Hand Fresh Plus", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH836802822.png"},
  {"code": "7106666", "name": "First Impression", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH10211480.png"},
  {"code": "7106865", "name": "Medallion", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH10218424.jpg"},
  {"code": "7103980", "name": "Oasis Pro Garden Sunshine/ Morning Breeze", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH7103978.png"},
  {"code": "7106115", "name": "Sanigard", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH833806500.png"},
  {"code": "7106104", "name": "Future DC", "image_url": "https://ecolabwallchart.azurewebsites.net/ecolab/img/product/TH834801920.png"}
]

filename = 'image_urls.json'
if os.path.exists(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
else:
    data = []

data.extend(new_data)

with open(filename, 'w') as f:
    json.dump(data, f, indent=2)
print("Appended", len(new_data), "items.")
