#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Eduardo Frazão
#   * http://github.com/fr4z40
#   * https://bitbucket.org/fr4z40

from bs4 import BeautifulSoup as bsp
from urllib.request import urlopen
from xlsxwriter import Workbook

def source(url_in):
    return(bsp((urlopen(url_in)).read()))


def get_events(html):
    ev = (((html.find_all('div',{'class':'row'}))[0]).find_all('div',{'class':'row'}))[0]
    ev = (ev.find_all('div',{'class':'col col-lg-3'}))
    for t in ev:
        thumbs = t.find_all('div',{'class':'thumbnail'})
        for tb in thumbs:
            nm = (((((tb.find_all('h3'))[0]).text).strip()).title())
            loc = (((((tb.find_all('strong'))[0]).text).strip()).title())
            print("%s ==> %s" % (nm, loc))
            rst.append((nm,loc))
    return(rst)



rst = []
url = 'http://www.wikifestivals.com/festivals'

while 1:
    html = source(url)
    get_events(html)
    nxt = html.find_all('li',{'class':'next last'})
    if (len(nxt) == 0):
        break
    else:
        nxt = ((nxt[0].find_all('a'))[0].get('href'))
        url = ('http://www.wikifestivals.com' + nxt)

rst = list(set(rst))
rst.sort()

print('Creating File...')
wb = Workbook('Events.xlsx')
ws = wb.add_worksheet('Locations')
bold = wb.add_format({'bold': True})
ws.write(0,0, 'Event Name', bold)
ws.write(0,1, 'Location', bold)
ws.set_column(0,0, 76)
ws.set_column(1,1, 50)

print('Saving...')
for r in range(len(rst)):
    ws.write((r+1),0, rst[r][0])
    ws.write((r+1),1, rst[r][1])

wb.close()