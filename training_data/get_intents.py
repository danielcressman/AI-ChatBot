from bs4 import BeautifulSoup
import json
import requests
import os
import sys

URL = "https://docs.google.com/document/d/e/2PACX-1vTFW4FvTMIt9XqwbgsC9issVMdTR4OlrHasUbLlcjfp2k7hjLwIF-bNwLAWm62TIAvAR5yFKqk_T5Rg/pub#h.r2si0xqsfiif"
GOOGLE_PREFIX = 'https://www.google.com/url?q='

page = requests.get(URL)

soup = BeautifulSoup(str(page.content, encoding='utf8'), "html.parser")

question_headers = soup.find_all("h2")

intents = []


def get_full_response_and_links(header):
    paragraphs = ""
    links = []
    next_element = header.next_sibling

    link_faq = False
    while next_element is not None and next_element.name != "h2":
        if "FAQ" in next_element.text:
            link_faq = True
        if next_element.text != '':
            paragraphs += next_element.text + '\n\n'
        for link in next_element.find_all('a'):
            suffix_index = link['href'].find('&sa=D')
            href_without_suffix = link.get('href')[:suffix_index]
            stripped_href = href_without_suffix.removeprefix(GOOGLE_PREFIX)
            links.append({'label': link.text, 'href': stripped_href})
        next_element = next_element.next_sibling

    if link_faq is True:
        links.insert(0, {'label': 'FAQ', 'href': URL})
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

dir_list = os.listdir('./topics')
for f in dir_list:
    if f.endswith('.json'):
        with open('./topics/' + f, "r") as topic_file:
            try:
                intents_for_topic = json.load(topic_file)
            except json.decoder.JSONDecodeError as json_error:
                print(f'json_error={json_error}')
                print(f'Error decoding {f}, exiting...')
                sys.exit()

        if isinstance(intents_for_topic, list):
            intents.extend(intents_for_topic)


output = {
    "intents": intents,
}

with open("intents.json", "w") as outfile:
    json.dump(output, outfile, indent=2)
