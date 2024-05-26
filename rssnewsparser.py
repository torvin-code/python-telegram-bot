import requests
import feedparser

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'

def get_new_posts(JSON_API_KEY, JSON_BIN):
    data = []
    setting = get_setting(JSON_API_KEY, JSON_BIN)
    if setting is None:
        data.append('Настройки не получены')
    if setting is not None:
        i = 0
        for rss in setting['rss']:
            item = get_rss(rss)
            if item is not None:
                setting['rss'][i]['last_news'] = item[0]['title']
                for post_item in item:
                    post = f"{post_item['title']}\n<a href=\"{post_item['url']}\">{post_item['url']}</a>"
                    data.append(post)
            i += 1
    upd_setting(JSON_API_KEY, JSON_BIN, setting)
    return(data)


def get_rss(rss):
    headers = {'user-agent': USER_AGENT}
    r = requests.get(rss['url'], headers=headers)
    a = r.status_code
    if a == 200:
        items = []
        d = feedparser.parse(r.text)
        for i in d.entries:
            if rss['last_news'] == i.title:
                break
            item = {"title": i.title, "url": i.link}
            items.append(item)
        if len(items) > 0:
            return items



def get_setting(JSON_API_KEY, JSON_BIN):
    url = f"https://api.jsonbin.io/v3/b/{JSON_BIN}/latest"
    headers = {
    'X-Master-Key': JSON_API_KEY,
    'X-Bin-Meta': 'false'
    }
    for x in range(3):
        req = requests.get(url, json=None, headers=headers)
        a = req.status_code
        if a == 200:
            data = req.json()
            if 'rss' in data.keys():
                return data
            


def upd_setting(JSON_API_KEY, JSON_BIN, setting):
    url = f"https://api.jsonbin.io/v3/b/{JSON_BIN}"
    headers = {
    'Content-Type': 'application/json',
    'X-Master-Key': JSON_API_KEY
    }
    for x in range(3):
        req = requests.put(url, json=setting, headers=headers)
        a = req.status_code
        if a == 200:
            break
