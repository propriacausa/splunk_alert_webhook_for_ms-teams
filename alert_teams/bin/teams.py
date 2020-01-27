import sys
import json
import urllib2
import csv
import gzip
from collections import OrderedDict


def send_webhook_teams(url, body, user_agent=None):
    if url is None:
        print >> sys.stderr, "ERROR No URL provided"
        return False
    print >> sys.stderr, "INFO Sending POST request to url=%s with size=%d bytes payload" % (url, len(body))
    print >> sys.stderr, "DEBUG Body: %s" % body
    try:
        req = urllib2.Request(url, body, {"Content-Type": "application/json", "User-Agent": user_agent})
        res = urllib2.urlopen(req)
        if 200 <= res.code < 300:
            print >> sys.stderr, "INFO Teams webhook receiver responded with HTTP status=%d" % res.code
            return True
        else:
            print >> sys.stderr, "ERROR Teams webhook receiver responded with HTTP status=%d" % res.code
            return False
    except urllib2.HTTPError, e:
        print >> sys.stderr, "ERROR Error sending Teams webhook request: %s" % e
    except urllib2.URLError, e:
        print >> sys.stderr, "ERROR Error sending Teams webhook request: %s" % e
    except ValueError, e:
        print >> sys.stderr, "ERROR Invalid URL: %s" % e
    return False


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] != "--execute":
        print >> sys.stderr, "FATAL Unsupported execution mode (expected --execute flag)"
        sys.exit(1)
    try:
        settings = json.loads(sys.stdin.read())
        url = settings['configuration'].get('url')
        # https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using#setting-up-a-custom-incoming-webhook
        body = OrderedDict()
        body['text'] = settings.get('result')['_raw']
        user_agent = settings['configuration'].get('user_agent', 'Splunk')
        if not send_webhook_teams(url, json.dumps(body), user_agent=user_agent):
            sys.exit(2)
    except Exception, e:
        print >> sys.stderr, "ERROR Unexpected error: %s" % e
        sys.exit(3)
