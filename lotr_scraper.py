
# The punkt model from nltk is needed, this only needs to be run once
# Certificate verify fix: https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download('punkt')

from nltk.tokenize import word_tokenize
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import codecs
import random
import re
import sys

def parse_book(url:str, start_title:str, use_parent=False):
    print("Reading URL", url)
    u = urlparse(url)
    corpus = []

    # Create soup
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    # Find the start of the book
    start = doc.find_all("h2", string=start_title)
    start_item = None
    for s in start:
        start_item = s
        
    if start_item == None:
        print("Failed to find start of the book")
        return None
    
    # Use the parent element if specified
    if use_parent:
        start_item = start_item.parent
    
    # Collect all paragraphs past the start of the book
    paragraphs = start_item.find_next_siblings([ "p", "blockquote" ])
    print("Found", len(paragraphs), "paragraphs")
    
    # Process paragraphs
    first_poem = None
    for paragraph in paragraphs:
        txt = paragraph.get_text().strip()
        
        # Skip blank lines
        if len(txt) <= 1:
            continue
        
        # Find and print the first poem, for fun :D
        if str(paragraph).startswith("<blockquote>") and first_poem is None:
            first_poem = txt
            
        # Tokenize and add to corpus
        tokens = word_tokenize(txt)
        tokens.insert(0, '<START>')
        tokens.append('<END>')
        corpus.append(tokens)
    
    print()
    print(first_poem)
    print()
    return corpus

def write_corpus(corpus, path):
    if corpus == None:
        print("Cannot write to file: corpus is null")
        return
    with codecs.open(path, 'w', 'utf-8') as f:
            f.write(str(corpus))
    
def main():
    url_book1 = "https://www.ae-lib.org.ua/texts-c/tolkien__the_lord_of_the_rings_1__en.htm"
    url_book2 = "https://www.ae-lib.org.ua/texts-c/tolkien__the_lord_of_the_rings_2__en.htm"
    url_book3 = "https://www.ae-lib.org.ua/texts-c/tolkien__the_lord_of_the_rings_3__en.htm"
    
    book1 = parse_book(url_book1, "Prologue", True)
    book2 = parse_book(url_book2, "Book III")
    book3 = parse_book(url_book3, "Book V")
    
    # List concatenation is alarmingly simple in Python
    complete = book1 + book2 + book3
    
    write_corpus(book1, "./lotr_book1.txt")
    write_corpus(book2, "./lotr_book2.txt")
    write_corpus(book3, "./lotr_book3.txt")
    write_corpus(complete, "./lotr_complete.txt")
    
if __name__ == '__main__':
    main()