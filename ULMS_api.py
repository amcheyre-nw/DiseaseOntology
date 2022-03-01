import requests
from lxml.html import fromstring
from cachetools import cached, TTLCache

TTL_7HRS = TTLCache(maxsize=2, ttl=25200)

class Auth:
    def __init__(self, api_key):
        self._api_key = api_key

    @cached(TTL_7HRS)
    def get_single_use_service_ticket(self):
        url = 'https://utslogin.nlm.nih.gov/cas/v1/api-key'
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
            'User-Agent': 'python'
        }
        resp = requests.post(
            url, data={'apikey': self._api_key}, headers=headers
        )
        resp.raise_for_status()
        html = fromstring(resp.text)
        ticket_granting_ticket_url = html.xpath('//form/@action')[0]

        resp = requests.post(
            ticket_granting_ticket_url,
            data={'service': 'http://umlsks.nlm.nih.gov'},
            headers=headers
        )
        resp.raise_for_status()
        single_use_service_ticket = resp.text
        return single_use_service_ticket


class API:
    BASE_URL = 'https://uts-ws.nlm.nih.gov/rest'

    def __init__(self, *, api_key, version='current'):
        self._auth = Auth(api_key=api_key)
        self._version = version
        self.api_key = api_key

    def get_cui(self, cui):
        self._auth = Auth(api_key=api_key) # need to call this multiple times? painful
        url = f'{self.BASE_URL}/content/{self._version}/CUI/{cui}'
        return self._get(url=url)

    def get_tui(self, tui):
        self._auth = Auth(api_key=self.api_key) # need to call this multiple times? painful
        url = (f'{self.BASE_URL}/semantic-network/{self._version}/TUI/{tui}')
        return self._get(url=url)

    def get_ui(self, ui):
        self._auth = Auth(api_key=self.api_key)  # need to call this multiple times? painful
        url = f'{self.BASE_URL}/content/{self._version}/source/MSH/{ui}'
        return self._get(url=url)

    def get_children(self, ui):
        self._auth = Auth(api_key=self.api_key) # need to call this multiple times? painful
        url = f'{self.BASE_URL}/content/{self._version}/source/MSH/{ui}/children'
        return self._get(url=url)

    def _get(self, url):
        ticket = self._auth.get_single_use_service_ticket()
        resp = requests.get(url, params={'ticket': ticket})
        resp.raise_for_status()
        return resp.json()


def build_tree(rootUI, _API):
    tree = [['class', 'superclass', 'class_UI']]
    leafs = []
    stack = [rootUI]
    root_str = ''
    while len(stack) > 0:
        print("building tree... stack size: {} | completed: {}".format(len(stack), len(tree)), flush=True, end='\r')
        ui = stack.pop(0)
        req = _API.get_ui(ui)
        if len(tree) == 1: # if we've just started add the top of the tree in
            tree.append([req['result']['name'], None, req['result']['ui']])

        child_req = _API.get_children(ui)
        children = [x for x in child_req['result']]
        #tree = tree + [[req['result']['name'], child['name']] for child in children]
        stack = [child['ui'] for child in children if child['children'] != 'NONE'] + stack # add children to stack if they also have children

        for child in children: # add the spo statements
            childname = child['name']
            parentname = req['result']['name']
            tree.append([childname, parentname, child['ui']])

            if child['children'] == "NONE":
                leafs.append([childname, child['ui']])
    return tree, leafs
