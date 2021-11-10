from bs4 import BeautifulSoup
import json
import requests
URL = "https://docs.google.com/document/d/e/2PACX-1vTFW4FvTMIt9XqwbgsC9issVMdTR4OlrHasUbLlcjfp2k7hjLwIF-bNwLAWm62TIAvAR5yFKqk_T5Rg/pub#h.r2si0xqsfiif"

page = requests.get(URL)

soup = BeautifulSoup(str(page.content, encoding='utf8'), "html.parser")

question_headers = soup.find_all("h2")

intents = []


def get_full_response_and_links(header):
  paragraphs = "" 
  links = []
  next_element = header.next_sibling

  while next_element != None and next_element.name != "h2":
    if next_element.text != '':
      paragraphs += next_element.text + '\n\n'
    for link in next_element.find_all('a'):
        links.append({'label': link.text, 'href': link.get('href')})
    next_element = next_element.next_sibling

  return paragraphs.strip(), links


def get_first_paragraph_response(header):
  return header.next_sibling.text

try:
    with open("extra_patterns.json", "r") as extra_patterns_file:
        extra_patterns = json.load(extra_patterns_file)
except IOError:
    extra_patterns = {}

for header in question_headers:
  questions = list(filter(lambda x: x.strip() != "", header.text.split("?")))
  answer, links = get_full_response_and_links(header)
  tag = questions[0].strip()

  # Remove ordinal from beginning of question
  questions[0] = ".".join(questions[0].split('.')[1:]) 
  
  # Remove any extra spaces
  questions = [question.strip() for question in questions]

  intents.append({
    "tag": tag,
    "patterns": questions + (extra_patterns[tag] if tag in extra_patterns else []),
    "responses": [answer],
    "links": links,
  })

output = {
    "intents": intents,
}

import json
with open("intents.json", "w") as f:
  json.dump(output, f, indent=2)
