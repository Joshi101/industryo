from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
import urllib.request as urllib2
from bs4 import BeautifulSoup
from .models import Company, Director


def scrape_za():
    domain = "https://www.zaubacorp.com"
    urls = "https://www.zaubacorp.com/company/A-A-AEROPARTS-LLP/"
    headers = {
        'Accept': 'text/css,*/*;q=0.1',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5 (Solaris 10) Gecko'
    }
    companies = Company.objects.all()[:100]

    for i in companies:
        url = urls + str(i.cin)
        print(url)
        try:
            response = urllib2.urlopen(url)
            soup = BeautifulSoup(response, "html.parser")
            try:
                # g = soup.findAll('p')
                # y3 = g[1].text.split(': ')[1]
                a = soup.findAll('div', attrs={'class': 'col-lg-6'})[2]

                # print(a)
                if '@' in a.text:
                    b = a.findAll('p')[0]
                    print(b)
                else:
                    print('NAHI HAI EMAIL')

            except Exception:
                print('FUCK')

        except Exception:
            print('More Fuck')
            # pass