import urllib.request
import urllib.parse

# Let's see if we can read the raw HTML of the PDV page from localhost
try:
    url = "http://127.0.0.1:5000/ponto-de-venda/index.html"
    req = urllib.request.Request(url)
    # Since we need to be logged in, we might get redirected to login. Let's see what we get.
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')
    print("STATUS CODE:", response.status)
    print("URL:", response.url)
    print("HTML length:", len(html))
    # Print the script tags
    for line in html.split('\n'):
        if 'script' in line or 'select2' in line:
            print(line.strip())
except Exception as e:
    print("Error:", e)
