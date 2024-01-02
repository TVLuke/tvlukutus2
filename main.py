# https://gist.github.com/aparrish/661fca5ce7b4882a8c6823db12d42d26
# https://mastodonpy.readthedocs.io/en/stable/
# https://github.com/jsvine/markovify

# https://shkspr.mobi/blog/2018/08/easy-guide-to-building-mastodon-bots/

import markovify
import time
from datetime import datetime
from mastodon import Mastodon
import json
from bs4 import BeautifulSoup

CLIENT_KEY = ""
CLIENT_SECRET = ""
ACCESS_TOKEN = ""


def load_conf():
    global CLIENT_KEY
    global CLIENT_SECRET
    global ACCESS_TOKEN
    f = open('conf.json')
    conf = json.load(f)
    CLIENT_KEY = conf["client-key"]
    CLIENT_SECRET = conf["client-secret"]
    ACCESS_TOKEN = conf["access-token"]


def remove_html_tags(input):
    soup = BeautifulSoup(input, 'html.parser')
    return soup.get_text()


def make_model():
    file2 = open('myfile.txt', 'w')
    tweet_list = []

    # Using readlines()
    file1 = open('tweets.js', 'r')
    lines = file1.readlines()

    _count = 0
    # Strips the newline character
    for line in lines:
        _count += 1
        striped_line = line.strip()
        if striped_line is not None and '"full_text" :' in striped_line:
            l2 = striped_line.replace('"full_text" :', "")
            l2 = l2.replace('\",', "")
            l2 = l2.replace('\n', "")
            l2 = l2.replace('\\', "")
            l2 = l2.replace('"', "")
            l2 = l2.strip()
            if '@' not in l2 and 'http' not in l2 and "\\" not in l2 and l2.count('. ') < 10:
                tweet_list.append(l2)

    f = open('outbox.json')
    mastodon = json.load(f)
    for item in mastodon['orderedItems']:
        if "https://www.w3.org/ns/activitystreams#Public" in item["to"]:
            toot_object = item["object"]
            print(toot_object)
            print(type(toot_object))
            print(">>> ")
            if type(toot_object) is dict and "https://www.w3.org/ns/activitystreams#Public" in toot_object['to']:
                print("===")
                content = remove_html_tags(toot_object['content'])
                if '@' not in content and 'http' not in content and "\\" not in content and content.count('. ') < 10:
                    print(content)
                    tweet_list.append(content)

    file2.write('\n'.join(tweet_list))
    file2.close()

    with open("myfile.txt") as f:
        text = f.read()

    # Build the model.
    # text_model = markovify.Text(text)
    _text_model = markovify.NewlineText(text, state_size=2)
    # text_model = markovify.Text(text, state_size=3)
    return _text_model


def clean_sentence(_sentence):
    if _sentence is not None:
        _sentence = _sentence.replace('.,', ". ")
        _sentence = _sentence.replace('?,', "? ")
        _sentence = _sentence.replace('!,', "! ")

        _sentence = _sentence.replace(',a', ", a")
        _sentence = _sentence.replace(',b', ", b")
        _sentence = _sentence.replace(',c', ", c")
        _sentence = _sentence.replace(',d', ", d")
        _sentence = _sentence.replace(',e', ", e")
        _sentence = _sentence.replace(',f', ", f")
        _sentence = _sentence.replace(',g', ", g")
        _sentence = _sentence.replace(',h', ", h")
        _sentence = _sentence.replace(',i', ", i")
        _sentence = _sentence.replace(',j', ", j")
        _sentence = _sentence.replace(',k', ", k")
        _sentence = _sentence.replace(',l', ", l")
        _sentence = _sentence.replace(',m', ", m")
        _sentence = _sentence.replace(',n', ", n")
        _sentence = _sentence.replace(',o', ", o")
        _sentence = _sentence.replace(',p', ", p")
        _sentence = _sentence.replace(',q', ", q")
        _sentence = _sentence.replace(',r', ", r")
        _sentence = _sentence.replace(',s', ", s")
        _sentence = _sentence.replace(',t', ", t")
        _sentence = _sentence.replace(',u', ", u")
        _sentence = _sentence.replace(',v', ", v")
        _sentence = _sentence.replace(',w', ", w")
        _sentence = _sentence.replace(',x', ", x")
        _sentence = _sentence.replace(',y', ", y")
        _sentence = _sentence.replace(',z', ", z")

        _sentence = _sentence.replace(',A', ", A")
        _sentence = _sentence.replace(',B', ", B")
        _sentence = _sentence.replace(',C', ", C")
        _sentence = _sentence.replace(',D', ", D")
        _sentence = _sentence.replace(',E', ", E")
        _sentence = _sentence.replace(',F', ", F")
        _sentence = _sentence.replace(',G', ", G")
        _sentence = _sentence.replace(',H', ", H")
        _sentence = _sentence.replace(',I', ", I")
        _sentence = _sentence.replace(',J', ", J")
        _sentence = _sentence.replace(',K', ", K")
        _sentence = _sentence.replace(',L', ", L")
        _sentence = _sentence.replace(',M', ", M")
        _sentence = _sentence.replace(',N', ", N")
        _sentence = _sentence.replace(',O', ", O")
        _sentence = _sentence.replace(',P', ", P")
        _sentence = _sentence.replace(',Q', ", Q")
        _sentence = _sentence.replace(',R', ", R")
        _sentence = _sentence.replace(',S', ", S")
        _sentence = _sentence.replace(',T', ", T")
        _sentence = _sentence.replace(',U', ", U")
        _sentence = _sentence.replace(',V', ", V")
        _sentence = _sentence.replace(',W', ", W")
        _sentence = _sentence.replace(',X', ", X")
        _sentence = _sentence.replace(',Y', ", Y")
        _sentence = _sentence.replace(',Z', ", Z")
        _sentence = _sentence.replace('  ', " ")
        _sentence = _sentence.replace('  ', " ")
        _sentence = _sentence.replace('  ', " ")
        _sentence = _sentence.replace('  ', " ")
        _sentence = _sentence.replace('  ', " ")
        _sentence = _sentence.replace('.nnund', ". Und")
        _sentence = _sentence.replace('lbeck', "Lübeck")
        _sentence = _sentence.replace('polize', "Polizei")

        _sentence = _sentence.replace(' 1.', "")

        _sentence = _sentence.capitalize()

        return _sentence


def make_a_toot(_text_model):
    for i in range(1):
        sentence = _text_model.make_short_sentence(max_chars=270)

        sentence = clean_sentence(sentence)

        print(sentence)

        api = Mastodon(CLIENT_KEY, CLIENT_SECRET, ACCESS_TOKEN, api_base_url="https://botsin.space")

        api.toot(sentence)


load_conf()
text_model = make_model()
while True:
    make_a_toot(text_model)
    for count in range(4680):
        time.sleep(10)
        now = datetime.now()
        print("now =", now)
        print(count)
