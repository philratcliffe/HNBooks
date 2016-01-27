import operator
import re
from urlparse import urlparse
import csv

# Pattern by Gruber for extracting URLs from a text string
GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
GRUBER_URLINTEXT_PAT = re.compile(r'https?://')
ISBN_10_PAT = re.compile(r'dp/([0-9]{9}[\d|X])')

# ISBN-10 pattern. Amazon seems to be using these in URLs for books.
ISBN_10_REGEX = r'/([0-9]{9}[\d|X])'

# File with Amazon URLs
TEXT_FILENAME = 'HNCommentsAll.json'

def save_dict(d):
    w = csv.writer(open("output.csv", "w"))

    # Iterate through the dictionary's key val pairs sorted by value (largest first)
    for key, val in iter(sorted(d.items(), key=operator.itemgetter(1), reverse=True)):
        w.writerow([key, val])

def read_file_in_chunks(file_object, chunk_size=4096):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def process_urls(isbns, d):
    for isbn in isbns:
        if isbn == "0321968972":
            print "another\n"
        d[isbn] = d.get(isbn, 0) + 1

def process_urls2(urls, d):
    for url in urls:
        if 'amazon' in url:
            parsed_url = urlparse(url)
            if parsed_url and parsed_url.hostname:
                if 'amazon.' in parsed_url.hostname:
                    m = re.search(ISBN_10_REGEX, url)
                    if m:
                        isbn = m.group(1)
                        d[isbn] = d.get(isbn, 0) + 1

    #with open(TEXT_FILENAME, 'r') as f:
    #    text = f.read()
    #    urls = [ mgroups[0] for mgroups in GRUBER_URLINTEXT_PAT.findall(text) ]

d = {}
f = open(TEXT_FILENAME, 'r')

for i, chunk in enumerate(read_file_in_chunks(f)):
    urls = ISBN_10_PAT.findall(chunk)
    process_urls(urls, d)
    save_dict(d)
    if i % 10000 == 0:
        print "========================================================"
        print i
        print(d)


