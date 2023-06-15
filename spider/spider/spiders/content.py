import scrapy
from pathlib import Path
from bs4 import BeautifulSoup
import configparser
import json
import PyPDF2

config = configparser.ConfigParser()
config.read('../config.ini')

name = "content"
allowed_domains = json.loads(config.get("default","allowed_domains"))
start_urls = json.loads(config.get("default","start_urls"))
main_domain = config['default']['main_domain']

def cleanAndWriteText(page, text):
    text = text.replace('\n', ' ')
    text = text.replace('\\n', ' ')
    text = text.replace('  ', ' ')
    text = text.replace('  ', ' ')
    text = text.strip()
    with Path(f"../data/txt/{page}.txt").open("w") as f:
        f.write(text)

class Spider(scrapy.Spider):
    name = name
    allowed_domains = allowed_domains
    start_urls = start_urls

    def parse(self, response):

        Path("../data/html").mkdir(parents=True, exist_ok=True)
        Path("../data/txt").mkdir(parents=True, exist_ok=True)
        Path("../data/pdf").mkdir(parents=True, exist_ok=True)

        url = response.url
        if 'redirect_urls' in response.request.meta:
            url = response.request.meta['redirect_urls'][0]

        page = "-".join(url.split("/")[2:])
        domain = url.split("/")[2]

        # is content type is pdf, then save the file
        if response.headers[b'Content-Type'] == b'application/pdf':
            Path(f"../data/pdf/{page}.pdf").write_bytes(response.body)
            reader = PyPDF2.PdfReader(f"../data/pdf/{page}.pdf")
            pages = []
            # join all content from all the pages in reader.pages
            for i in range(0, len(reader.pages)):
                pages.append(reader.pages[i].extract_text())
            
            text = " ".join(pages)
            cleanAndWriteText(page, text)


        else:
            Path(f"../data/html/{page}.html").write_bytes(response.body)

            soup = BeautifulSoup(response.body, "html.parser")
            text = soup.get_text()
            cleanAndWriteText(page, text)
            
            self.log(f"Saved file {page}")

            for href in response.xpath("//a/@href").getall():
                if href.startswith("http") and domain==main_domain:
                    yield scrapy.Request(response.urljoin(href), self.parse)

