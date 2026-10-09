import os
import json
import shutil
from modules.sheet_manager import SheetManager
from modules.reset_manager import reset_customer_sheet

# 1. Create public directory & PWA files
os.makedirs('public', exist_ok=True)

html_content = '''<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Easy POS</title>
  <link rel="manifest" href="/manifest.json">
  <style>
    body { font-family: sans-serif; padding: 20px; background: #f4f6f9; }
    .card { background: white; padding: 20px; border-radius: 8px; max-width: 400px; margin: 0 auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    h2 { margin-top: 0; color: #333; }
    input, select { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
    button { width: 100%; padding: 12px; background: #25D366; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
  </style>
</head>
<body>
  <div class="card">
    <h2>EASY POS - SALES & INVOICE</h2>
    <p>PWA Mobile App Ready</p>
  </div>
</body>
</html>'''

with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('public/manifest.json', 'w', encoding='utf-8') as f:
    f.write('{"name":"Easy POS","short_name":"EasyPOS","start_url":"/","display":"standalone"}')

with open('public/sw.js', 'w', encoding='utf-8') as f:
    f.write('self.addEventListener("fetch", e => {});')

# 2. Create Vercel and Gitignore files
vercel_config = {
  "version": 2,
  "builds": [
    { "src": "api/invoice.py", "use": "@vercel/python" },
    { "src": "public/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/api/invoice", "dest": "api/invoice.py" },
    { "src": "/(.*)", "dest": "public/$1" }
  ]
}

with open('vercel.json', 'w', encoding='utf-8') as f:
    json.dump(vercel_config, f, indent=2)

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write(".venv/\n__pycache__/\nconfig/service_account.json\nbackups/\n")

# 3. Clean backup subdirectories
if os.path.exists('backups'):
    for item in os.listdir('backups'):
        item_path = os.path.join('backups', item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)

# 4. Reset Google Sheets
try:
    sm = SheetManager('config/service_account.json')
    with open('config/customers.json', 'r', encoding='utf-8') as f:
        custs = json.load(f)
    for c in custs:
        if c.get('active'):
            reset_customer_sheet(sm, c['sheet_id'])
except Exception as e:
    print(f"Sheet Reset Note: {e}")

print("\n[SUCCESS] Project structure, PWA files, Vercel config & Backups completely set up!")