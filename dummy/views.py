from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
import urllib.request as urllib2
from bs4 import BeautifulSoup
from .models import Company,Director


def scrape_za():
    domain = "http://www.indisearch.com"
    urls = "http://www.indisearch.com/ecreations-india-pvt-ltd/"
    headers = {
        'Accept': 'text/css,*/*;q=0.1',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5 (Solaris 10) Gecko'
    }
    lis = list(range(446714, 500000))

    for i in lis:
        url = urls + str(i)
        print(url)
        try:
            response = urllib2.urlopen(url)
            soup = BeautifulSoup(response, "html.parser")
            try:
                g = soup.findAll('p')
                y3 = g[1].text.split(': ')[1]

                if '@' in y3:
                    a = soup.findAll('h1', attrs={'class': 'htext'})
                    b = soup.findAll('div', attrs={'class': 'paddress'})[0].text.split('Phone:')
                    k1 = b[0].strip()
                    k2 = b[1].split('Fax')[0].strip()
                    y1 = a[0].string
                    y2 = g[0].text.split(': ')[1]
                    y4 = g[2].text.split(': ')[1]
                    y5 = g[3].text.strip()
                    y6 = g[4].text
                    indi = Company.objects.create(name=y1, person=y2, email=y3, city=y4, z=i, business_categories=y5,
                                                   business_work=y6, address=k1, phone=k2)

                else:
                    print(i)
            except Exception:
                print('FUCK')

        except Exception:
            print('More Fuck')
            # pass