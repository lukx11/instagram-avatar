import re
import requests
import bs4
import urllib
from datetime import datetime
link = 'https://www.instagram.com/accounts/login/'
login_url = 'https://www.instagram.com/accounts/login/ajax/'
time = int(datetime.now().timestamp())
payload = {
    'username': 'USERNAME',
    'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:PASSWORD',
    'queryParams': {},
    'optIntoOneTap': 'false'
}
with requests.Session() as s:
    r = s.get(link, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_3 rv:3.0; sl-SI) AppleWebKit/533.38.2 (KHTML, like Gecko) Version/5.0 Safari/533.38.2'})
    csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
    r = s.post(login_url, data=payload, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    })
    print(r.status_code)
    if r.status_code == 200:
        print(r.text)
        nazwa = input("wprowadz nazwe uzytkownika: ")
        pagee = 'https://www.instagram.com/' + nazwa + '/?__a=1'
        page = s.get(pagee, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_7_3 rv:3.0; sl-SI) AppleWebKit/533.38.2 (KHTML, like Gecko) Version/5.0 Safari/533.38.2'})
        soup = bs4.BeautifulSoup(page.content, "html.parser")
        #match = re.search(r'"profile_pic_url_hd":"https://instagram([^\"]+)', str(soup))
        #itsit = match.group(0)[22:].replace(r"&amp;", "&")
        #print(match.group(0)[22:].replace(r"&amp;", "&"))
        f = open(f'{nazwa}.jpg', 'wb')
        f.write(urllib.request.urlopen(page.json()["graphql"]["user"]["profile_pic_url_hd"]).read())
        f.close()
        print("Post downloaded successfully!")
        print("Full name: "+page.json()["graphql"]["user"]["full_name"])
        print("Biografia: "+page.json()["graphql"]["user"]["biography"])
        if page.json()["graphql"]["user"]["is_private"] == False:
            print("profil jest publiczny! czy chcesz pobrac zdjecia?")
    else:
        print("error :/ "+ r.text)
