import unittest
import translator
import conceptualizer

class translaTest(unittest.TestCase):
    def test_titleTrans(self):
        test = { 'title' : "Ciao Mondo!"}
        self.assertEqual(translator.to_english(test, "it")['en_title'], "Hello World!")

class concepTest(unittest.TestCase):
    def test_conceptTitle(self):
        test = { 'title' : "Ciao Mondo!", 'date' : "2021-10-20", 'language' : "it", 'source' : "ilPost", 'en_title' : "Hello World!"}
        self.assertEqual(conceptualizer.conceptualize(test)['concepts'][0]['word'], "World")

if __name__ == "__main__":
    unittest.main()