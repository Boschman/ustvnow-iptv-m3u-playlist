import sys
import requests
import cookielib
from bs4 import BeautifulSoup
import json

def Ustvnow(user, password, free_or_all):
    stations=["ABC", "CBS", "CW", "FOX", "NBC", "PBS", "My9"]
    if free_or_all == 'all':
        stations.extend(["AETV", "AMC", "Animal Planet", "Bravo", "Cartoon Network", "CNBC", "CNN", "Comedy Central", "Discovery Channel", "ESPN", "Fox News Channel", "FX", "History", "Lifetime", "National Geographic Channel", "Nickelodeon", "SPIKE TV", "Syfy", "TBS", "TNT", "USA"])
    d = {}
    cj = cookielib.CookieJar()
    url = "http://m.ustvnow.com/iphone/1/live/login"
    payload = {'username': user, 'password': password, 'device':'gtv', 'redir':'0'}
    with requests.Session() as s:
        r = s.post(url, data=payload)
    html = r.text
    j = json.loads(html)
    token = j['token']
    m3u8playlist =  "#EXTM3U\n"
    cj = cookielib.CookieJar()
    url = "http://m.ustvnow.com/iphone/1/live/login"
    payload = {'username': user, 'password': password, 'device':'gtv', 'redir':'0'}
    with requests.Session() as s:
        r = s.post(url, data=payload)
        R = s.get("http://m.ustvnow.com/iphone/1/live/playingnow")
    html = R.text
    try:
        soup = BeautifulSoup(html,"lxml")
    except:
        soup = BeautifulSoup(html,"html.parser")
    for tag in soup.findAll('div'):
        if tag.has_attr('sname'):
            sname = tag["sname"]
            sname = sname.replace(" ","")
            title = ' '.join(html.split())
            title = title[ title.find(sname) : title.find(sname) + 200 ]
            title = title[ title.find("<h1>") + 4 : title.find("</h1>")]
            title = title.replace(" ","")
            d[title]=sname
    for station in stations:
        station = station.replace(" ","")
        url = "http://m.ustvnow.com/iphone/1/live/viewlive?streamname="+d[station]+"&stream_origin=ilv10.oedg.ustvnow.com&app_name=ilv10&token="+token+"&passkey=tbd&extrato=tbd"
        r = s.get(url)
        html =  r.text
        try:
            soup = BeautifulSoup(html,"lxml")
        except:
            soup = BeautifulSoup(html,"html.parser")
        link = "None"
        for tag in  soup.findAll('video'):
            link = str(tag['src'])
            m3u8playlist += "#EXTINF:-1," + station + "\n"
            m3u8playlist += link+ "\n"
            try:
                f = open(station+".strm","w")
                f.write(link)
                f.close()
            except:
                pass
    return m3u8playlist.rstrip("\n")

if len(sys.argv) == 4:
    username = sys.argv[1]
    password = sys.argv[2]
    free_or_all = sys.argv[3]

    print(Ustvnow(username,password,free_or_all))
else:
    print("Usage: python main.py [username] [password] [free|all]")
