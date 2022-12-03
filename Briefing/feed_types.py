import feedparser
def refresh_rss(feed):
    url = feed.url
    feed = feedparser.parse(url)
    return feed["entries"]

def refresh_atom(source):
    return None

def refresh_rest(source):
    return None