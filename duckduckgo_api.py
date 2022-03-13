from duckduckgo_search import ddg


def get_wikititle_from_queery(queery, site='en.wikipedia.org'):
    '''

    API to leverage duckduckgo's NLP in its search engine to find the title of a wikipedia page if the wikipedia api
    fails to do so.

    Example is "Concentration camp syndrome" which doesn't exist in wikipedia directly, but is represented on a wiki
    page with another name: "Survivors guilt". Our wiki api fails here, but this addition will allow our scraper to make
    the link.

    :param queery: queery being searched. String.
    :param site: website to get results from.... choose wikipedia pls
    :return: title of the most relevant wikipedia page to the queery
    '''
    try:
        result = ddg("{} site:{}".format(queery, site))
        title = result[0]['title']

        #quirk -> the page has a string ' - Wikipedia' on the end. Remove it.
        title = title.replace(' - Wikipedia', '')
        return title
    except:
        return None

if __name__ == '__main__':
    print("See how duckduckgo can find the wikipedia page on Concentration Camp Syndrome, by finding"
          "\n its alternative name: Survivor Guilt")
    print(get_wikititle_from_queery('Concentration camp syndrome'))
