# coding=UTF-8

import unittest

from keybert import KeyBERT


class KeyBertTest(unittest.TestCase):
    def testExtractWords(self) -> None:
        doc: str = """
The first-gen Subaru BRZ was introduced more than a decade ago alongside its mechanical sibling, the Toyota 86, forever changing the world of entry-level sports cars. Before the arrival of the BRZ, the light and affordable sports car scene was rather limited, with the evergreen Mazda MX-5 Miata dominating. But the BRZ has heralded a new age and promises massive fun, reliability, and even some practicality for not so many dollars, and was all-new for the 2022 model year.

The 2023 BRZ features a 2.4-liter Boxer engine with 228 horsepower and 184 lb-ft of torque, which is more than enough to get this two-door coupe moving. Power is sent to the rear wheels via a slick six-speed transmission which buyers can opt to row themselves. The amount of fun you can have with the BRZ borders on illegal. Subaru BRZ competitors include the Toyota GR86 and the aforementioned icon from Mazda. Ford's Mustang and the Chevy Camaro offer much more power, but can also be looked at if you want a 2+2 coupe with RWD and a manual transmission. We think you might linger over the BRZ, though - and we don't blame you.
        """
        doc2: str = """
BERT is a method of pre-training language representations. Pre-training refers to how BERT is first trained on a large source of text, such as Wikipedia. You can then apply the training results to other Natural Language Processing (NLP) tasks, such as question answering and sentiment analysis.        
        """
        kw_model: KeyBERT = KeyBERT()
        keywords: list[tuple[str, float]] | list[list[tuple[str, float]]] = kw_model.extract_keywords([doc,doc2])
        for keyword in keywords:
            print("keyword: {}, distance: {}".format(keyword[0], keyword[1]))
