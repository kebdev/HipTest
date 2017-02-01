__author__ = 'kevin'

from ..msg import extract_content


# activate the environment and cd to tests/
# run this command:
#   py.test test_msg.py

# start of pytest tests for regression
def test_mentions():
    msg = '@chris you around?'
    actual = extract_content(msg)
    expected = """{
  "mentions": [
    "chris"
  ]
}"""
    assert(actual == expected)


def test_emoticons():
    msg = 'Good morning! (megusta) (coffee)'
    actual = extract_content(msg)
    expected = """{
  "emoticons": [
    "megusta",
    "coffee"
  ]
}"""
    assert(actual == expected)


def test_links():
    msg = 'Olympics are starting soon; http://www.nbcolympics.com'
    actual = extract_content(msg)
    expected = """{
  "links": [
    {
      "url": "http://www.nbcolympics.com",
      "title": "2018 PyeongChang Olympic Games | NBC Olympics"
    }
  ]
}"""
    assert(actual == expected)


def test_all():
    msg = '@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016'
    actual = extract_content(msg)
    expected = """{
  "mentions": [
    "bob",
    "john"
  ],
  "emoticons": [
    "success"
  ],
  "links": [
    {
      "url": "https://twitter.com/jdorfman/status/430511497475670016",
      "title": "Justin Dorfman on Twitter: &quot;nice @littlebigdetail from @HipChat (shows hex colors when pasted in chat). http://t.co/7cI6Gjy5pq&quot;"
    }
  ]
}"""
    assert(actual == expected)


def test_dup_links():
    msg = 'Hello https://www.google.com and https://www.google.com'
    actual = extract_content(msg)
    expected = """{
  "links": [
    {
      "url": "https://www.google.com",
      "title": "Google"
    },
    {
      "url": "https://www.google.com",
      "title": "Google"
    }
  ]
}"""
    assert(actual == expected)


# start of inline unit tests
def run_test(msg):
    content = extract_content(msg)
    print content
    print
    return


def run_tests():
    run_test('@chris you around?')
    run_test('Good morning! (megusta) (coffee)')
    run_test('Olympics are starting soon; http://www.nbcolympics.com')
    run_test('@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016')
    run_test('Hello https://www.google.com and https://www.google.com')  # test caching
    return

# cd to directory above hiptest
# ensure that environment is activated
# run the command:
#    python -m hiptest.tests.test_msg
if __name__ == '__main__':
    run_tests()

