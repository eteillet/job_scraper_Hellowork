import json
from bs4 import BeautifulSoup
import requests
import urllib
import re
from datetime import datetime
import os
import pandas as pd

RESULT_FILE_PATH='results.json'

def get_context(title: list, location: list, page: int):
    """
    - define the url we want to request (type of job, location ...)
    - get the html content of the page ready to parse
    """
    get_options = {'k': title, 'l': location, 'c': 'Stage', 'p': page}
    url = 'https://www.hellowork.com/fr-fr/emploi/recherche.html?' + urllib.parse.urlencode(get_options)
    agent = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"}   
    response = requests.get(url, headers=agent)
    soup = BeautifulSoup(response.content, "html.parser")
    job_soup = soup.find(class_="crushed content")
    return job_soup

def get_title(job_elem):
    return job_elem.find('h3').get_text(strip=True)

def get_company(job_elem):
    return job_elem.find('span', {'data-cy': 'companyName'}).get_text(strip=True)

def get_contract(job_elem):
    return job_elem.find('span', {'data-cy': 'contract'}).get_text(strip=True)

def get_location(job_elem):
    return job_elem.find('div', {'data-cy': 'loc'}).get_text(strip=True)

def get_date(job_elem):
    return job_elem.find('span', {'data-cy': 'publishDate'}).get_text(strip=True)

def get_url(job_elem):
    return 'https://www.hellowork.com' + job_elem.find('a')['href']

def extract_job_details(job, job_elem):
    job['title'] = get_title(job_elem)
    job['company'] = get_company(job_elem)
    job['contract'] = get_contract(job_elem)
    job['location'] = get_location(job_elem)
    job['date'] = get_date(job_elem)
    job['url'] = get_url(job_elem)
    return job

def scrap_job_informations(soup):
    """ scraps informations for each job """
    data = []
    jobs = soup.find_all(class_=re.compile("offer--content"))
    for elem in jobs:
        job = dict()
        job = extract_job_details(job, elem)
        if job['location'] != 'France':
            data.append(job)
    return data

def scrap(titles: list, locations: list):
    data_collected = []
    for title in titles:
        for location in locations:
            page = 1
            while True:
                soup = get_context(title, location, page)
                if soup == None:
                    break
                jobs = scrap_job_informations(soup)
                data_collected.extend(jobs)
                page += 1
    with open('results.json', 'a') as fp:
        json.dump(data_collected, fp, sort_keys=False, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if os.path.isfile(RESULT_FILE_PATH):
        os.remove(RESULT_FILE_PATH)
    titles = ["data", "python"]
    locations = ["Vendee", "Nantes"]
    scrap(titles, locations)