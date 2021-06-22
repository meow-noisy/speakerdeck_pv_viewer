# scrape speakerdeck.com users daily pv and create a csv file.

from pathlib import Path

import csv
import requests
from bs4 import BeautifulSoup

url = "https://speakerdeck.com/meow_noisy"


r = requests.get(url)

html = r.text
soup = BeautifulSoup(html, "lxml")


container = soup.select(".container.py-md-4.py-3")[0]
slides = container.select(
    '.row.mb-4')[0].select(".col-12.col-md-6.col-lg-4.mb-5")

l = []
for slide in slides:
    slide_id = slide.select(".card.deck-preview")[0]["data-id"]
    slide_title = slide.find('a')["title"]

    elem = slide.find('div')
    elem.select('.row.mb-4')
    span = elem.find("span")
    pv = span["title"].replace(" views", "")
    l.append([slide_id, slide_title, pv])

    # import pdb
    # pdb.set_trace()
#slides = soup.find('tbody')

from datetime import datetime
dt_now = datetime.now()
str_dt_now = dt_now.strftime('%Y-%m-%d')
print(str_dt_now)
p = Path(f"result/{str_dt_now}.tsv")
p.parent.mkdir(exist_ok=True, parents=True)


with p.open('w') as f:
    writer = csv.writer(f, delimiter='\t')
    for record in l:
        writer.writerow(record)
