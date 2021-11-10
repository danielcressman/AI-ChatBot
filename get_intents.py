from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
URL = "https://docs.google.com/document/d/e/2PACX-1vTFW4FvTMIt9XqwbgsC9issVMdTR4OlrHasUbLlcjfp2k7hjLwIF-bNwLAWm62TIAvAR5yFKqk_T5Rg/pub#h.r2si0xqsfiif"

page = requests.get(URL)

soup = BeautifulSoup(unidecode(str(page.content, encoding='utf8')), "html.parser")

question_headers = soup.find_all("h2")

intents = []


def get_full_response(header):
  paragraphs = "" 
  next_span = header.next_sibling

  while next_span != None and next_span.name != "h2":
    paragraphs += next_span.text
    next_span = next_span.next_sibling

  return paragraphs


def get_first_paragraph_response(header):
  return header.next_sibling.text


for header in question_headers:
  questions = list(filter(lambda x: x.strip() != "", header.text.split("?")))
  answer = get_full_response(header)
  tag = questions[0].strip()

  # Remove ordinal from beginning of question
  questions[0] = ".".join(questions[0].split('.')[1:]) 
  
  # Remove any extra spaces
  questions = [question.strip() for question in questions]

  intents.append({
    "tag": tag,
    "patterns": questions,
    "responses": [answer]
  })

output = {
    "intents": intents,
}

import json
with open("intents.json", "w") as f:
  json.dump(output, f, indent=2)
