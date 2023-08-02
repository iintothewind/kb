# coding=UTF-8

import unittest
import re

from keybert import KeyBERT

kw_model: KeyBERT = KeyBERT()


def remove_brackets(text: str, brackets: str = "()[]") -> str:
    if text:
        count = [0] * (len(brackets) // 2)  # count open/close brackets
        saved_chars = []
        for character in text:
            for i, b in enumerate(brackets):
                if character == b:  # found bracket
                    kind, is_close = divmod(i, 2)
                    count[kind] += (-1) ** is_close  # `+1`: open, `-1`: close
                    if count[kind] < 0:  # unbalanced bracket
                        count[kind] = 0  # keep it
                    else:  # found bracket to remove
                        break
            else:  # character is not a [balanced] bracket
                if not any(count):  # outside brackets
                    saved_chars.append(character)
        return ''.join(saved_chars).strip()
    return ""


def remove_special_chars(text: str) -> str:
    if text:
        c = re.sub('[^a-zA-z0-9/\-]+', ' ', text)
        return c
    return ""


def extract_keywords(text: str) -> str:
    text = text.lower() if text else ""
    if text and len(text.split(" ")) > 5:
        keywords = kw_model.extract_keywords(text.lower())
        return " ".join([kw[0] for kw in keywords])
    return text



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
