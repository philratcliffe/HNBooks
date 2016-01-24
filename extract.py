import re
from urlparse import urlparse

# Pattern by Gruber for extracting URLs from a text string

GRUBER_URLINTEXT_PAT = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

ISBN_10_REGEX = r'/([0-9]{9}[\d|X])' # Amazon seems to be using these in the URL of books

with open('test_data', 'r') as f:
    text = f.read()
    urls = [ mgroups[0] for mgroups in GRUBER_URLINTEXT_PAT.findall(text) ]

for url in urls:
    parsed_url = urlparse(url)
    if parsed_url and parsed_url.hostname:
        if 'amazon.' in parsed_url.hostname:
            m = re.search(ISBN_10_REGEX, url)
            if m:
                isbn = m.group(1)
                print isbn
            print url[:80]

