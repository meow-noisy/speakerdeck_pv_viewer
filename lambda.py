
# scrape speakerdeck.com users daily pv and create a csv file.

from pathlib import Path

import csv
import requests
from bs4 import BeautifulSoup
import boto3
from datetime import datetime


s3 = boto3.resource('s3')


def lambda_handler(event, context):

    bucket = 'YOUR S3 BUCKET'
    url = "https://speakerdeck.com/ your speakerdeck account"

    r = requests.get(url)

    html = r.text
    soup = BeautifulSoup(html, "lxml")

    container = soup.select(".container.py-md-4.py-3")[0]
    slides = container.select(
        '.row.mb-4')[1].select(".col-12.col-md-6.col-lg-4.mb-5")

    l = []
    for slide in slides:
        slide_id = slide.select(".card.deck-preview")[0]["data-id"]
        slide_title = slide.find('a')["title"]

        elem = slide.find('div')
        elem.select('.row.mb-4')
        span = elem.find("span")
        pv = span["title"].replace(" views", "")
        l.append([slide_id, slide_title, pv])

    dt_now = datetime.now()
    str_dt_now = dt_now.strftime('%Y-%m-%d')
    print(str_dt_now)
    p = Path(f"result/{str_dt_now}.tsv")
    tmp_path = Path("/tmp") / p
    tmp_path.parent.mkdir(exist_ok=True, parents=True)

    with tmp_path.open('w') as f:
        writer = csv.writer(f, delimiter='\t')
        for record in l:
            writer.writerow(record)
    key = str(p)

    obj = s3.Object(bucket, key)
    obj.upload_file(str(tmp_path))
    return
