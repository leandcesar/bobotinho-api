# -*- coding: utf-8 -*-
import re

from app.services import BaseService


class Utils(object):

    @staticmethod
    def remove_tags(html):
        new_text = ""
        tag = False
        for char in html:
            if not tag and char == "<":
                tag = True
            elif not tag:
                new_text += char
            elif tag and char == ">":
                tag = False
        return new_text

    @staticmethod
    def text_between(text, before, after):
        start = text.find(before)
        if start > -1:
            start += len(before)
        if before[-1] != ">":
            start = text.find(">", start) + 1
        end = text.find(after, start)
        if after[0] != "<":
            end = text.find("<", start)
        if -1 < start < end:
            return text[start:end]
        return ""

    @staticmethod
    def remove_spaces(text):
        text = text.replace("\t", " ")
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        while text.find("  ") > -1:
            text = text.replace("  ", " ")
        return text.strip()

    @staticmethod
    def remove_accents(text):
        reference = [('a', 'áàâãä'), ('e', 'éèêë'), ('i', 'íìîï'), ('o', 'óòôõö'), ('u', 'úùûü'), ('c', 'ç')]
        new_text = ""
        for char in text:
            for clear_vowal, possible_accents in reference:
                if char in possible_accents:
                    new_text += clear_vowal
                    break
            else:
                new_text += char
        return new_text

    @staticmethod
    def split_html_tag(text, tag):
        return list(filter(None, re.split(f'<[^>]*{tag}[^>]*>', text)))


class Dicio(dict):

    def __init__(self, page):
        meaning, etymology, word_class = self.scrape_meaning(page)
        self.word = self.scrape_word(page)
        self.synonyms = self.scrape_synonyms(page)
        self.meaning = meaning
        self.etymology = etymology
        self.word_class = word_class

    def scrape_word(self, page):
        return Utils.text_between(page, "<h1", "</h1>").lower()

    def scrape_meaning(self, page):
        html = Utils.text_between(page, 'class="significado', '</p>')
        word_class = Utils.text_between(html, 'class="cl', '</span>')
        word_class = Utils.remove_spaces(Utils.remove_tags(word_class))
        etymology = Utils.text_between(html, 'class="etim', '</span>')
        etymology = Utils.remove_spaces(Utils.remove_tags(etymology))
        meaning = Utils.split_html_tag(html, 'span')
        meaning = [Utils.remove_spaces(Utils.remove_tags(x)) for x in meaning]
        meaning = " ".join([x for x in meaning if x and x != etymology]).replace(word_class, "").replace(etymology, "")
        return meaning, etymology, word_class

    def scrape_synonyms(self, page):
        synonyms = []
        if page.find('class="adicional sinonimos"') > -1:
            html = Utils.text_between(page, 'class="adicional sinonimos"', '</p>')
            while html.find('<a') > -1:
                synonym = Utils.text_between(html, '<a', '</a>')
                synonym = Utils.remove_spaces(synonym).strip().lower()
                synonyms.append(synonym)
                html = html.replace('<a', "", 1).replace('</a>', "", 1)
        return ", ".join(synonyms)

    def as_dict(self) -> dict:
        return {
            "word": self.word,
            "meaning": self.meaning,
            "etymology": self.etymology,
            "synonyms": self.synonyms,
            "word_class": self.word_class,
        }


class DicioService(BaseService):
    url = "http://www.dicio.com.br"

    def definition(self, word: str) -> dict:
        word = Utils.remove_accents(word).lower()
        data = self.http_get(f"{self.url}/{word}", res_type="html")
        dicio = Dicio(data).as_dict()
        return dicio
