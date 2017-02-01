__author__ = 'kevin'

from ..msg import extract_content


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

# cd to directory above hipchat
# ensure that environment is activated
# run the command:
#    python -m hipchat.tests.test_msg
if __name__ == '__main__':
    run_tests()

