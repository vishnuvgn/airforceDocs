import requests, time, re, os, json
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome()
'''
code runs on azure virtual machine
'''

count = 1
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver.get('https://catalog.gpo.gov')

def start():

    form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'form1'))
    )
    inputField = form.find_element(By.NAME, 'request')
    inputField.send_keys('air force') # human variable
    inputField.send_keys(Keys.RETURN)


def getTableContents():
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.opac_pulled_info > table:nth-child(11)'))
    )

    rows = table.find_elements(By.TAG_NAME, 'tr')
    headerRow = rows[0]
    bodyRows = rows[1:]

    for row in bodyRows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        # (counting from 0)
        # 2nd column is the title
        # 6th column is the link that we need
        
        index = cells[0].text
        title = cells[2].text
        year = cells[3].text
        author = cells[4].text
        link = cells[6].text
        
        if link != "":
            filewrite(index, title, year, author, link)
            

def clean_title(title):
    # Remove parentheses and their contents
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'[\[\]\(\)]', '', title)
    title = title.replace("/", "")
    
    # Remove leading and trailing whitespace
    title = title.strip()
    title = title[:100]
    
    # Replace spaces with empty string

    return title


def nextPage():
    try:
        nextButton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.opac_pulled_info > div:nth-child(13)'))
        )
        nextButton = nextButton.find_element(By.CSS_SELECTOR, '[title="Next"]')
        
        nextButton.click()
        return True
    except:
        print('No more pages')
        return False

def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])



def filewrite(index, title, year, author, link):
    
    if not is_valid_url(link):
        return

    file = requests.get(link)
    if file.url.endswith('.pdf'):
        global count
        print(f'{index}) {link} -- #{count}')
        count += 1
        title = clean_title(title)

        innerFolderPath = f'./docs/{index}'
        os.mkdir(innerFolderPath)

        with open(f'{innerFolderPath}/{title}.pdf', 'wb') as f:
            f.write(file.content)

        with open(f'{innerFolderPath}/metadata.json', 'w') as f:
            metadata = {
                "author": author,
                "year": year,
            }
            json.dump(metadata, f)

'''
name
date
format
calculated title
key words
people (authors, citations)
people (mentioned, connected)
people (titles, roles)
tag line, hashtags
companies
short description
long description (abstract)
pages / source -- where in the document is the information, give me excerpt
department, agency, organization, etc.


synthetic data -- verticals
'''


boolVar = True
start()
while boolVar:
    getTableContents()
    boolVar = nextPage()
    time.sleep(2)

driver.quit()