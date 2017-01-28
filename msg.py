
from bs4 import BeautifulSoup
import re

import requests

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
    links = URL_REGEX.findall(chat_msg)
    logger.debug("links = " + str(links))

    link_titles = []
    for link in links:
        r = requests.get(link)
        if 200 <= r.status_code < 300:
            soup = BeautifulSoup(r.text)
            # any other entity substitutions?
            if soup.title:
                title = re.sub(pattern='\"', repl='&quot;', string=soup.title.string)
            else:
                title = "Not Found"
            link_title = {
                'url': link,
                'title': title
            }
            link_titles.append(link_title)
        else:
            logger.info("Link {0} returned status {1}".format(link, r.status_code))

    logger.debug("link_titles = " + str(link_titles))

    return link_titles

def run_test(msg):
    # import libraries only needed for tests; so don't import it at the top
    import json
    from collections import OrderedDict

    print 'Input: "{}"'.format(msg)
    print "Return:"
    mentions, emoticons, links = extract_content(msg)

    # replacement for jsonify since that requires a Flask request context
    output_map = OrderedDict()
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



