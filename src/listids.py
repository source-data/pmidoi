import re
import argparse
import requests
from xml.etree.ElementTree import fromstring

class NotValidIDError(Exception):
    def __init__(self, id, message):
       self.id = id
       self.message = message


class ID:
    '''
    An identifier.
    '''
    id_regexp = ''
    reg = re.compile(id_regexp)
    _str = None
    
    def __init__(self, s: str):
        self.check(s)
        self._str = s

    @classmethod
    def check(cls, s):
        try:
            assert isinstance(s, str)
        except:
            raise NotValidIDError(s, 'not a string')
        try:
            assert cls.reg.match(s)
        except:
            raise NotValidIDError(s, 'does not match ' + cls.id_regexp)

    def __str__(self):
        return self._str

class DOI(ID):
    id_regexp = r'^10.\d{4,9}/[-._;()/:a-zA-Z0-9]+$'
    reg = re.compile(id_regexp)

class PMID(ID):
    id_regexp = r'^\d+$'
    reg = re.compile(id_regexp)


class JournalTitle:
    '''
    The title of a Journal
    '''

    _title = ''

    def __init__(self, text):
        self._title = str(text)
    
    def __str__(self):
        return self._title

class Journal:
    '''
    Created with a JournalTitle, populates  set of PMID
    '''

    def __init__(self, journal_title:str):
        self.title = JournalTitle(journal_title)

    def list_article(self, page_size=1000):
        articles = []
        next_cursor_mark = '*'
        page = 1
        print()
        while True:
            response = EuropePMC.search_publications(self.title, cursorMark=next_cursor_mark, pageSize=page_size).json()
            results = response['resultList']['result']
            hit_count = int(response['hitCount'])
            if results:
                articles += [Article(r) for r in results]
                next_cursor_mark = response['nextCursorMark']
                print(f"total: {hit_count} | page: {page} from {1+ (hit_count // page_size)}   ")
                page += 1
            else:
                break
        assert len(articles) == hit_count, f"len(results) {len(articles)} != hit_count {hit_count}"    
        return articles


class Article:

    def __init__(self, j):
        try:
            self.doi = DOI(j['doi'])
        except KeyError:
            self.doi = None
        try:
            self.pmid = PMID(j['pmid'])
        except KeyError:
            self.pmid = None

class TabbedIDs:

    def __init__(self, article_list):
        self.article_list = article_list
    
    def format(self, article_list, delim="\t", eol="\n"):
        l = [delim.join([str(a.pmid), str(a.doi)]) for a in article_list]
        s = eol.join(l)
        return s

    def save(self, filename):
        s = self.format(self.article_list)
        with open(filename, 'w') as f: 
            f.write(s)
            print(f"\n\nResults saved to {filename}.\n\n")

class EuropePMC:
    '''
    Mini API to EuroPMC webservice.
    '''

    base_url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
    search_fields = {'journal_title':'JOURNAL', 'ext_id':'EXT_ID'}

    @staticmethod
    def build_journal_title_query(journal_title: JournalTitle):
        return EuropePMC.search_fields['journal_title'] + ":" + '"' + str(journal_title) + '"'
    
    @staticmethod
    def req(query: str, **params):
        params = dict(params)
        params['query'] = query
        r = requests.get(EuropePMC.base_url, params)
        return r
    
    @staticmethod
    def search_publications(journal_title: JournalTitle, **kwargs) -> requests.Response:
        query = EuropePMC.build_journal_title_query(journal_title)
        r = EuropePMC.req(query, resultType='lite', format='json', **kwargs)
        return r

def main():
    parser = argparse.ArgumentParser(description='Extracting pmid - doi table for a given journal.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('journal_title', help='The title of the journal')
    parser.add_argument('save_to', nargs='?', default='pmidoi.txt', help='The file to save the extracted id list.')
    args = parser.parse_args()
    journal_title = args.journal_title
    filename = args.save_to
    journal = Journal(journal_title)
    articles = journal.list_article()
    pmid_doi = TabbedIDs(articles)
    pmid_doi.save(filename)

if __name__ == '__main__':
    main()