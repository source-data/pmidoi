import unittest
from src.converter import NotValidIDError, DOI, PMID, EuropePMC, JournalTitle, Journal, Article, TabbedIDs

class TestConverter(unittest.TestCase):

    def setUp(self):
        self.valid_doi_str = '10.15252/msb.20188339'
        self.invalid_doi_str = '10_15252-msb.20188339'
        self.valid_journal_name = "The EMBO Journal"
    
    def test_doi_check(self):
        with self.assertRaises(NotValidIDError):
            DOI(self.invalid_doi_str)
    
    def test_doi_create(self):
        doi = DOI(self.valid_doi_str)
        self.assertEqual(self.valid_doi_str, str(doi))

    def test_build_journal_title_query(self):
        the_embo_journal = JournalTitle('The EMBO Journal')
        self.assertEqual(EuropePMC.build_journal_title_query(the_embo_journal), 'JOURNAL:"The EMBO Journal"')

    def test_search_publications(self):
        response = EuropePMC.search_publications(self.valid_journal_name)
        self.assertEqual(response.status_code, 200)

    def test_journal_list_pmid(self):
        lsa = Journal('Life Science Alliance')
        articles = lsa.list_article(page_size=25)
        self.assertEqual(len(articles), 163)

        empty = Journal('')
        articles = empty.list_article()
        self.assertEqual(len(articles), 0)

    def test_article_list(self):
        with self.assertRaises(NotValidIDError):
            corrupted_article_list = [
                Article({'doi':'asdf', 'pmid': '1234'}),
                Article({'doi':2, 'pmid': '12345678'}),
            ]

        article_list = [
            Article({'doi':'10.1234/2338', 'pmid': '12345678'}),
            Article({'doi':'10.4321/aer1234', 'pmid': '87654321'}),
        ]
        
        tab_list = "12345678\t10.1234/2338\n87654321\t10.4321/aer1234"

        self.assertEqual(TabbedIDs(article_list).out(), tab_list)

if __name__ == '__main__':
    unittest.main()