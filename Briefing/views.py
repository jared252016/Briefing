from django.shortcuts import render
import os
from django.conf import settings
from django.contrib.auth.models import User 
from .models import Tab,Feed
from urllib.parse import urlparse
import urllib.request
from datetime import datetime,timezone
import json
from django.views.decorators.csrf import csrf_exempt
import feedparser
from django.http import HttpResponse

def now_diff(last_scan):
    delta = datetime.now(timezone.utc) - last_scan
    return delta.total_seconds() / (60 * 60)

def create_widget_newsfeed_item(_item):
    item = { 
        'title': _item.title,
        'url': _item.link,
        'description': _item.summary
    }
    return item

def refresh_feed(feed):
    url = feed.url
    url_= urlparse(url)
    file = url_.hostname.replace(".", "_") + url_.path.replace("/", "_")
    urllib.request.urlretrieve(url, os.path.join(settings.BASE_DIR, "Briefing/feeds/"+file))
    feed.file = file
    feed.date_last_scan = datetime.now(timezone.utc)
    feed.save()
    return feed

def create_widget_newsfeed(widget):

    feed = Feed.objects.get(pk=widget["feed"])
    obj = {
        "title": widget["name"],
        "count": 0,
        "entries": [],
        "last_scan": feed.date_last_scan,
        "template": "widget_news_feed.html",
        "feed": widget["feed"]
    }

    if now_diff(feed.date_last_scan) >= 1:
        feed = refresh_feed(feed)
    path = os.path.join(settings.BASE_DIR, "Briefing/feeds/"+feed.file)
    feed = feedparser.parse(path)
    obj["count"] = len(feed["entries"][:10])
    for _item in feed["entries"][:10]:
        obj["entries"].append(create_widget_newsfeed_item(_item))
    return obj

def create_widget_blank():
    obj = {
        "template": "widget_blank.html",
        "widget": ""
    }
    return obj

def create_widget(type, widget):
    if type.startswith("widget_news_feed"):
        return create_widget_newsfeed(widget)
    elif type.startswith("widget_blank"):
        return create_widget_blank(widget)
    else:
        return create_widget_blank(widget)

def index_create_context():
    w_context = []
    tab = Tab.objects.get(user_id=1)
    widgets = json.loads(tab.widgets)
    for column in widgets:
        col = []
        for widget in column:
            obj = create_widget(widget["template"], widget)
            col.append(obj)
        w_context.append(col)
    return {"widgets":w_context}

@csrf_exempt
def update_tab(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        tab = Tab.objects.get(user_id=1)
        tab.widgets = body_unicode
        tab.save()
        return HttpResponse('{"message":"success"}')

def index(request): 
    context = index_create_context()
    template_name="index.html"
    return render(request, template_name, context)
