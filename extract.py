import operator
import re
import csv

import ConfigParser

from amazon.api import AmazonAPI

ISBN_10_PAT = re.compile(r'dp/([0-9]{9}[\d|X])')

# ISBN-10 pattern. Amazon seems to be using these in URLs for books.
ISBN_10_REGEX = r'/([0-9]{9}[\d|X])'

# File containing downloaded HN data (postings and comments)
HN_DATA_FILENAME = 'HNCommentsAll.json'

# A file containing Amazon credentials in the following format
# [Credentials]
# AMAZON_ACCESS_KEY:
# AMAZON_SECRET_KEY:
# AMAZON_ASSOC_TAG:

AMAZON_CREDENTIALS_FILE = '.amazon_credentials'


def save_dict(d):
    """Write the dictionary in CSV format to a file"""
    w = csv.writer(open("output.csv", "w"))

    # Iterate through the dictionary's key value pairs sorted by value
    # (largest first)
    for key, val in iter(sorted(d.items(), key=operator.itemgetter(1), reverse=True)):
        w.writerow([key, val])


def read_file_in_chunks(file_object, chunk_size=4096):
    """Generator to read the potentially huge data file"""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def process_isbns(isbns, d):
    """Count up the occurrences of each ISBN"""
    for isbn in isbns:
        d[isbn] = d.get(isbn, 0) + 1


def ConfigSectionMap(section):
    """Helper function for accessing the config file"""
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

config = ConfigParser.ConfigParser()
print config.read(AMAZON_CREDENTIALS_FILE)
print config.sections()
print ConfigSectionMap("Credentials")["amazon_access_key"]


d = {}

# Open the file containing all the HN data (entries, comments etc)
f = open(HN_DATA_FILENAME, 'r')

# Look for an ISBN in URLs and keep track of those found
for i, chunk in enumerate(read_file_in_chunks(f)):
    isbns = ISBN_10_PAT.findall(chunk)
    process_isbns(isbns, d)
    save_dict(d)
    if i % 10000 == 0:
        print "========================================================"
        print i
        print(d)
