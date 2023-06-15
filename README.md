# Spider Chatbot

This project will crawl and scrape content from websites and pages you specify to create a corpus of text that will be used as context for a question answering agent. This uses the embeddings API from OpenAI to calculate embeddings for the content. The embeddings and context is saved in a CSV file.  The CSV file is used to create context to send along with the question to retrieve an answer from OpenAI. 

## Pre-requisites

You will need an OpenAI API key to get started. 

## 1. Create the config file

Copy `config.sample.ini` to `config.ini` and customize. 

```ini
[default]
model = text-davinci-003
openaiApiKey = sk-nnnnnn
allowed_domains =  [
    "yourwebsite.dev"
    ]
start_urls = [
    "https://yourwebsite.dev/index.html"
    ]
main_domain = yourwebsite.dev

```

## 2. Set up your python environment

```bash
python -m venv env

source env/bin/activate

pip install -r requirements.txt
```

## 3. Crawling

```bash
cd spider
scrapy crawl content
```

## 4. Create embeddings

```bash
python embeddings.py
```

## 5. Start and test API

1. Start API
```bash
FLASK_APP=api.py flask run
```

2. Test API
```bash
curl --location 'http://127.0.0.1:5000/' \
--header 'Content-Type: application/json' \
--data '{"question":"who are you?"}'
```


