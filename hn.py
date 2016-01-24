"""Downloads items from HN

"""

from hackernews import HackerNews
import string


hn = HackerNews()

with open('amazon.txt','w') as f:
    for i in range(50, 20000):
        item = hn.get_item(i)
        if item.text:
            s = item.text
            s = filter(lambda x: x in string.printable, s)
            if 'amazon' in s:
                print s
                print type(s)
                f.write(s)
                f.flush()
                f.write("\n")


