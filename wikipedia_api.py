import requests
from bs4 import BeautifulSoup
import bs4
import wikipediaapi
import re
import pandas as pd
from tqdm import tqdm
import duckduckgo_api as ddg_wrapper

def getData_from_wikiInfoBox(url, infobox_item, delimeter="hyperlinks"):
    '''

    Function pulls a infobox_item value from wikipedia's InfoBox, from URL
    :param url: URL of wikipedia page
    :param infobox_item: the label within the InfoBox that we're scraping the value of (eg: "Symptoms")
    :param delimeter: either "hyperlinks" to scrape only text associated with hyperlinks, "," to split text by commas,
    or None to pull whole text in one block
    :return: list of the InfoBox data (formatted nicely)
    '''

    url_name = url.split('/')[-1].replace('_', ' ')

    if infobox_item == 'wiki_name':
        return [url_name]

    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    lhs = soup.find_all('th', {"class":"infobox-label"}) # get lhs of the InfoBox
    lhs_bool = [c.text == infobox_item for c in lhs]
    rhs = soup.find_all('td', {"class":"infobox-data"}) # rhs of InfoBox
    itemsHTML = rhs[lhs_bool.index(True)]

    if delimeter=="hyperlinks":
        itemsText = [i.text for i in itemsHTML.find_all('a')]
    elif delimeter==",":
#        itemsText = itemsHTML.getText('<br/>').split('<br/>')
        # new lines in contents are defined by <br/> and not <a>. Stitch <a> instances back up with text
#        _itemsText = [i.text for i in itemsText]
#        itemsText = []
#        for i in range(1, len(itemsText)):
#            if _itemsText[i] != '' and _itemsText[i-1] != '':
#                itemsText = itemsText + [_itemsText[i-1] + ' ' + _itemsText[i]]

#        itemsText = [i for i in itemsText if not isinstance(i, bs4.element.Tag)]
        itemsText = [itemsHTML.text]
        itemsText = [i.lower().replace(' and ', ' ') for i in itemsText]
        itemsText = [i.replace(' or ', ' ') for i in itemsText]
        itemsText = [i.split(". ") for i in itemsText]
        itemsText = [item for sublist in itemsText for item in sublist] # flatten
        itemsText = [i.split('; ') for i in itemsText] # this will be a list of lists... need to flatten
        itemsText = [item for sublist in itemsText for item in sublist] # flatten
        itemsText = [i.split(', ') for i in itemsText] # this will be a list of lists... need to flatten
        itemsText = [item for sublist in itemsText for item in sublist] # flatten
        itemsText = [re.sub(r'\[[^()]*?\]', '', i) for i in itemsText]
    else:
        #itemsText = re.sub(r'\[[0-9]+]', '', itemsHTML.text)
        itemsText = [re.sub(r'\[[^()]*?\]', '', itemsHTML.text)]
        itemsText = [i.replace('  ', ' ') for i in itemsText] # get rid of any double spaces

    regex = re.compile(r'\[[0-9]+]') # remove references like '[13]'
    itemsText = [i for i in itemsText if not regex.match(i)]
    regex = re.compile(r'\[[^()]*?\]') # remove references like '[13]'
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
    labels = [l.text for l in lhs] + ['wiki_name'] # always add our own "wiki_name" label in... represents the name
                                                    # of the condition given in the URL
    return labels


def get_wikiURL_from_title(title, duckduckgo_backup=False):
    '''
    :param title: title of wikipedia page (string)
    :param duckduckgo_backup: Bool: if True, if wikipedia fails to find a page, use duckduckgo to find the most relevant
    wiki page to use.
    :return: URL of wiki page
    '''
    wiki_wiki = wikipediaapi.Wikipedia('en') # english
    page_py = wiki_wiki.page(title)
    try:
        return page_py.fullurl
    except(KeyError):
        if duckduckgo_backup:
            ddg_title = ddg_wrapper.get_wikititle_from_queery(title)
            wiki_wiki_ddg = wikipediaapi.Wikipedia('en')
            page_py = wiki_wiki_ddg.page(ddg_title)
            try:
                return page_py.fullurl
            except:
                pass
        else:
            return None


def get_wiki_summary(disease):
    '''
    retrieves the body text from wikipedia entry on disease
    :param disease:  disease/label to search wikipedia for
    :return:
    '''
    wiki_wiki = wikipediaapi.Wikipedia('en') # english
    page = wiki_wiki.page(disease)

    summary = page.summary.split(' ')
    summary_lower = [s.lower() for s in summary]
    return summary_lower


def retrieveFacts(disease, label, delimeter='hyperlinks', duckduckgo_backup=False):
    '''
    Wrapper of above functions for ease of use. Returns the data associated with a disease/label.
    Eg: disease = "Arthritis", label = "Symptoms" will return a list of symptoms associated with Arthritis
    :param disease: disease name (string)
    :param label: descriptor of what we want to retrieve about the disease (ie: Symptoms)
    :param delimeter: see getData_from_wikiInfoBox documentation
    :param duckduckgo_backup: Bool: if True, if wikipedia fails to find a page, use duckduckgo to find the most relevant
    wiki page to use.
    :return: list of "fact"s concerning the disease
    '''
    url = get_wikiURL_from_title(disease, duckduckgo_backup=duckduckgo_backup)
    label = '{}{}'.format(label[0].upper(), label[1:].lower()) # ensure correct formatting
    try:
        return getData_from_wikiInfoBox(url, label, delimeter=delimeter)
    except:
        return None


def retrieveLabels(disease):
    '''
    Wrapper of above functions for ease of use. Gives list of possible labels we can scrape from Wikipedia, for
    a given disease.
    :param disease: Name of disease
    :return: list of available labels
    '''
    url = get_wikiURL_from_title(disease)
    if url:
        return getLabels_from_wikiInfoBox(url)
    else:
        return None


def histogram_of_labels(diseases, pctg=False):
    '''

    :param diseases: list of diseases to look up
    :param pctg: if True, histogram returned contains % of dataset, if False, it returns raw count
    :return: histogram of all labels associated with these diseases, in histogram format
    '''

    histogram = pd.DataFrame(index=None, columns=['disease', 'label'])
    for d in tqdm(diseases):
        labels = retrieveLabels(d)
        if labels is not None:
            for l in labels:
                histogram.loc[len(histogram)] = [d, l]

    histogram = histogram.groupby('label').agg('count')
    if pctg:
        histogram = pd.DataFrame(histogram).rename(columns={'disease': '% occurence'})
        pctgs = (histogram.astype('float')/len(diseases)*100).sort_values(by='% occurence', ascending=False).round(1)
        pctgs['% occurence'] = pctgs['% occurence'].astype('str') + '%'
        return pctgs
    else:
        histogram = pd.DataFrame(histogram).rename(columns={'disease': 'Number of occurences'})
        return histogram.sort_values(by='Number of occurences', ascending=False)


if __name__ == '__main__':
    x = get_wikiURL_from_title("concentration camp syndrome", duckduckgo_backup=True)
    print(x)
