import os

from bs4 import BeautifulSoup

# Scrapes the CSES website
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller

# Checks if chrome driver is already in path, if not installs and adds it to path.
chromedriver_autoinstaller.install()

# CSES base URL
cses_base_url = "https://cses.fi/problemset/list/"

options = Options()
options.add_argument('--headless=old')

# Selenium browser
browser = webdriver.Chrome(options=options)


def scrape_cses():
    browser.get(cses_base_url)
    # Wait for the main div
    WebDriverWait(browser, 1).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, ".content")))

    problem_types = browser.find_elements(by=By.TAG_NAME, value="ul").copy()
    categories = browser.find_elements(by=By.TAG_NAME, value="h2")
    categories_text = []
    for category in categories:
        categories_text.append(category.text.lower().replace(' ', '_'))

    # skip over the first one since it includes elements that are irrelevant to this project
    sub_requests = []
    for i in range(2, len(problem_types)):
        list_elems = problem_types[i].find_elements(
            By.TAG_NAME, value="li").copy()
        category = categories_text[i-1]

        path = os.path.join("categories", category)
        if not os.path.exists(os.path.join("categories", category)):
            os.makedirs(path)

        for elem in list_elems:
            link = elem.find_element(By.TAG_NAME, "a")
            link_text = link.text
            link_ref = link.get_property("href")
            sub_requests.append((link_ref, link_text, path))

    for request in sub_requests:
        scrape_problem(*request)


def scrape_problem(url: str, problem_name: str, path: str):
    browser.get(url)
    WebDriverWait(browser, 1).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, ".content")))
    main = browser.find_element(By.CSS_SELECTOR, ".content")
    html = main.get_attribute("innerHTML")
    markdown = markdownify(html)

    file_path = os.path.join(path, problem_name + ".md")
    with open(file_path, 'w+', encoding="utf-8") as file:
        file.write(markdown)


def markdownify(html: str):
    # Use soup for the rest
    soup = BeautifulSoup(html, 'html.parser')

    removable_tags = ['title', 'link', 'script', 'input', 'math', 'mrow', 'mi']
    unwrappable_tags = ['span', 'ul']

    # Unwrap tags that we want to preserve contents but not necessarily do any
    # extra processing with
    for tag in unwrappable_tags:
        for sp in soup.find_all(tag):
            sp.unwrap()

    # Remove tags that we don't care about.
    for tag in removable_tags:
        for i in soup.find_all(tag):
            i.decompose()

    for par in soup.find_all('p'):
        par.replace_with(par.text + "\n")

    for bold in soup.find_all('b'):
        bold.replace_with(boldify(bold.text))

    for header in soup.find_all('h1'):
        header.replace_with(headerify('h1', header.text))

    for block in soup.find_all('pre'):
        block.replace_with(code_blockify(block.text))

    for div in soup.find_all('div'):
        div.replace_with("\n" + div.text)

    output = ""
    for otag in soup.contents:
        if otag == "\n":  # decomposing tags will leave us with bunch of empty line tags
            continue
        output += otag.text + "\n"
    return output.rstrip()


def boldify(text):
    return "**" + text + "**"


def headerify(h, text):
    return "#" * int(h[1]) + " " + text + "\n"


def code_blockify(text):
    return "```\n" + text + "```\n"


scrape_cses()
