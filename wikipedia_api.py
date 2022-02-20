import requests
from bs4 import BeautifulSoup
import wikipediaapi
import re

def getData_from_wikiInfoBox(url, infobox_item):
    '''

    Function pulls a infobox_item value from wikipedia's InfoBox, from URL
    :param url: URL of wikipedia page
    :param infobox_item: the label within the InfoBox that we're scraping the value of (eg: "Symptoms")
    :return: list of the InfoBox data (formatted nicely)
    '''
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    lhs = soup.find_all('th', {"class":"infobox-label"}) # get lhs of the InfoBox
    lhs_bool = [c.text == infobox_item for c in lhs]
    rhs = soup.find_all('td', {"class":"infobox-data"}) # rhs of InfoBox
    itemsHTML = rhs[lhs_bool.index(True)]
    itemsText = [i.text for i in itemsHTML.find_all('a')]

    regex = re.compile(r'\[[0-9]+]') # remove references like '[13]'
    itemsText = [i for i in itemsText if not regex.match(i)]

    items = [i[0].upper() + i[1:].lower() for i in itemsText] # format capital letters
    return items


def getLabels_from_wikiInfoBox(url):
    '''

    Returns list of the labels presented in the InfoBox on wikipedia's page specified by URL
    :param url: URL of wikipedia page
    :return: list of the labels present in the wikipedia InfoBox
    '''

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    lhs = soup.find_all('th', {"class":"infobox-label"}) # get lhs of the InfoBox
    labels = [l.text for l in lhs]
    return labels


def get_wikiURL_from_title(title):
    '''

    :param title: title of wikipedia page (string)
    :return: URL of wiki page
    '''
    wiki_wiki = wikipediaapi.Wikipedia('en') # english
    page_py = wiki_wiki.page(title)
    return page_py.fullurl


def retrieveFacts(disease, label):
    '''

    wrapper of above functions for ease of use. Returns the data associated with a disease/label.
    Eg: disease = "Arthritis", label = "Symptoms" will return a list of symptoms associated with Arthritis
    :param disease: disease name (string)
    :param label: descriptor of what we want to retrieve about the disease (ie: Symptoms)
    :return: list of "fact"s concerning the disease
    '''
    url = get_wikiURL_from_title(disease)
    label = '{}{}'.format(label[0].upper(), label[1:].lower()) # ensure correct formatting
    return getData_from_wikiInfoBox(url, label)


def retrieveLabels(disease):
    '''

    wrapper of above functions for ease of use. Gives list of possible labels we can scrape from Wikipedia, for
    a given disease.
    :param disease: Name of disease
    :return: list of available labels
    '''
    url = get_wikiURL_from_title(disease)
    return getLabels_from_wikiInfoBox(url)


print("Possible labels for type 2 diabetes: ", retrieveLabels("Type II Diabetes"))
# notice it doesn't matter whether I put II or 2... both point to the same place
print("\nSymptoms for type 2 diabetes: ", retrieveFacts("Type 2 Diabetes", "Symptoms"))