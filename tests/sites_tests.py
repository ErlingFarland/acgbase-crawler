import unittest

import mwclient

from lib.sites import wikipedia_ja, wikipedia_zh, moegirl


class MyTestCase(unittest.TestCase):
    def run_test(self, site: mwclient.Site):
        page = site.pages
        print(next(iter(site.pages)))

    def test_wikipedia_ja(self):
        self.run_test(wikipedia_ja())

    def test_wikipedia_zh(self):
        self.run_test(wikipedia_zh())

    def test_moegirl(self):
        self.run_test(moegirl())


if __name__ == '__main__':
    unittest.main()
