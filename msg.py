
from bs4 import BeautifulSoup
import re

import certifi
import urllib3
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

import os
import logging
import logging.handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # must be set to lowest level of all handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)      # display error and critical on the console so they can be viewed in realtime
ch.setFormatter(formatter)
logger.addHandler(ch)

logfile = os.getcwd() + os.sep + 'msg.log'
fh = logging.handlers.TimedRotatingFileHandler(logfile, when='midnight', backupCount=7)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

def extract_content(chat_msg):
    logger.debug("Extracting content from: " + chat_msg)
    mentions = get_mentions(chat_msg)
    emoticons = get_emoticons(chat_msg)
    links = get_links(chat_msg)
    return mentions, emoticons, links

def get_mentions(chat_msg):
    at_mentions = re.findall('@[a-zA-Z]{1,15}', chat_msg)
    mentions = [x[1:] for x in at_mentions]    # strip off leading '@' sign
    logger.debug("mentions = " + str(mentions))
    return mentions

def get_emoticons(chat_msg):
    paren_emoticons = re.findall('\([a-zA-Z]{1,15}\)', chat_msg)
    emoticons = [x[1:-1] for x in paren_emoticons]
    logger.debug("emoticons = " + str(emoticons))
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
                'title': soup.title.string if soup.title else "Not Found"
            }
            link_titles.append(link_title)
        else:
            logger.info("Link {0} returned status {1}".format(link, r.status))

    logger.debug("link_titles = " + str(link_titles))

    return link_titles

def run_test(msg):
    # import libraries only needed for tests; so don't import it at the top
    import json
    # !!from bs4.dammit import EntitySubstitution
    # !!esub = EntitySubstitution()

    print 'Input: "{}"'.format(msg)
    print "Return:"
    mentions, emoticons, links = extract_content(msg)

    # replacement for jsonify since that requires a Flask request context
    for link in links:
        escaped = re.sub(pattern='\"', repl='&quot;', string=link['title'])
        link['title'] = escaped
    output_map = {}
    if mentions:
        output_map['mentions'] = mentions
    if emoticons:
        output_map['emoticons'] = emoticons
    if links:
        output_map['links'] = links

    # print unit test output
    print json.dumps(output_map, indent=2, separators=(',', ': '))
    print
    return

def run_tests():
    run_test('@chris you around?')
    run_test('Good morning! (megusta) (coffee)')
    run_test('Olympics are starting soon; http://www.nbcolympics.com')
    run_test('@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016')
    return

if __name__ == '__main__':
    run_tests()



