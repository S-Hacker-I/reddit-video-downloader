import json

def json_to_netscape(json_file, netscape_file):
    with open(json_file, 'r') as f:
        cookies = json.load(f)
    
    with open(netscape_file, 'w') as f:
        f.write("# Netscape HTTP Cookie File\n")
        f.write("# This is a generated file! Do not edit.\n\n")
        
        for cookie in cookies:
            domain = cookie.get('domain')
            path = cookie.get('path', '/')
            secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
            expiry = int(cookie.get('expirationDate', 0))
            name = cookie.get('name')
            value = cookie.get('value')
            
            # Handle missing expirationDate
            if not expiry:
                expiry = 0
            
            line = f"{domain}\tTRUE\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n"
            f.write(line)

# Convert your JSON cookies file to Netscape format
json_to_netscape('tiktok_cookies.json', 'tiktok_cookies.txt')
