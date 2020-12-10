import re, os, lxml, socket, requests, time, sys
import pandas as pd
from lxml.html import fromstring
import urllib.request, urllib.error, urllib.parse

socket.getaddrinfo('localhost', 8080)

def crawl_country(url_path):
    r = requests.get(url_path)
    root = lxml.html.fromstring(r.content)
    hrefs = root.xpath('//a[not(starts-with(@href, "../"))]/@href')
    myfile = open('data/countrylist.csv', 'w')
    for href in hrefs:
        if href.endswith('.htm'):
            myfile.writelines("%s\n" % href)
            print(href)
    myfile.close()

def crawl_city(url_path):
    r = requests.get(url_path)
    root = lxml.html.fromstring(r.content)
    hrefs = root.xpath('//a[contains(@href, "/play/")]/@href')
    myfile = open('data/city.csv', 'w')
    yy = re.search('\/[a-z]{2}\/', url_path).group(0)
    for href in hrefs:
        ss = re.search('\/[a-z]{2}\/', href).group(0)
        if  ss == yy:
            x = href.replace("../", 'http://worldradiomap.com/')
            print(x)
            myfile.writelines("%s\n" % x)
    myfile.close()

def crawl_radios():
    data = pd.read_csv('data/city.csv')
    myfile = open('data/streams.csv', 'w')
    for index, row  in data.iterrows():
        r = requests.get(row[0])
        root = lxml.html.fromstring(r.content)
        stream_url = root.xpath('//div[@id="playlist"]/a/@href')[0]
        stream_url = stream_url.split('.m3u')[0]
        radio_name = os.path.splitext(os.path.basename(row[0]))[0]
        line = str(radio_name)+","+str(stream_url)
        print(line)
        myfile.writelines("%s\n" % line)
        try:
            detect_audio(stream_url, radio_name)
        except Exception as e:
            pass
            print('Error could not fetch stream')

    myfile.close()

def detect_audio(url,fname):
    print('Connecting to ' + url)
    response = urllib.request.urlopen(url, timeout=10.0)
    f = open('audio/'+fname+ '.wav', 'wb')
    block_size = 1024
    print('Recording audio please wait')
    limit = 10
    start = time.time()
    while time.time() - start < limit:
 #       try:
            audio = response.read(block_size)
#            if not audio:
#                print('Error could not fetch stream')
            f.write(audio)
            sys.stdout.write('.')
            sys.stdout.flush()
#        except Exception as e:
#            pass
#            print('Error' + e + 'could not fetch stream')

    f.close()
    sys.stdout.flush()
    print('\n audio has been recorded in ' + fname)
