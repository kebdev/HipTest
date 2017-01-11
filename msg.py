
from bs4 import BeautifulSoup
import re
import certifi
import urllib3
import urllib3.contrib.pyopenssl

urllib3.contrib.pyopenssl.inject_into_urllib3()

def extract_content(chat_msg):
    mentions = get_mentions(chat_msg)
    emoticons = get_emoticons(chat_msg)
    links = get_links(chat_msg)
    return mentions, emoticons, links

def get_mentions(chat_msg):
    at_mentions = re.findall('@[a-zA-Z]{1,15}', chat_msg)
    mentions = [x[1:] for x in at_mentions]    # strip off leading '@' sign
    return mentions

def get_emoticons(chat_msg):
    paren_emoticons = re.findall('\([a-zA-Z]{1,15}\)', chat_msg)
    emoticons = [x[1:-1] for x in paren_emoticons]
    return emoticons

def get_links(chat_msg):

    URL_REGEX = re.compile(
        # protocol identifier
        u"(?:(?:https?|ftp)://)"
        # user:pass authentication
        u"(?:\S+(?::\S*)?@)?"
        u"(?:"
        # IP address exclusion
        # private & local networks
        u"(?!(?:10|127)(?:\.\d{1,3}){3})"
        u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
        u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
        u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
        u"|"
        # host name
        u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        u")"
        # port number
        u"(?::\d{2,5})?"
        # resource path
        u"(?:/\S*)?"
        , re.UNICODE)

    links = URL_REGEX.findall(chat_msg)

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    
    link_titles = []
    for link in links:
        r = http.request('GET', link)
        if r.status == 200 or r.status == 201:
            soup = BeautifulSoup(r.data)
            link_title = { 
                'url': link, 
                'title': soup.title.string
            }
            link_titles.append(link_title)
 
    return link_titles

def run_tests():
    import json     # only needed for tests, so don't import it at the top
    print "test1: ", get_mentions('@chris you around?')
    print "test2: ", get_emoticons('Good morning! (megusta) (coffee)')
    print "test3: ", get_links('Olympics are starting soon; http://www.nbcolympics.com')
    mentions, emoticons, links = extract_content('@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016')
    print "test4: ", json.dumps([mentions, emoticons, links], indent=4, separators=(',', ': '))
    pass

if __name__ == '__main__':
    run_tests()



