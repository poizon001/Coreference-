import HTMLParser
html_parser = HTMLParser.HTMLParser()

import string
import itertools
import re
from appos import appos
from slangs import slangs
from emoticons import emo
import urllib
import urlparse
from urllib2 import HTTPError
from urllib2 import URLError
import json

def decode_it(text):
	return text.decode("utf-8").encode("ascii","ignore")
	
def escape(text):
    return html_parser.unescape(text)

def emoticons_look_up(text):
	words = text.split()
	emolist = []
	for word in words:
		if word in emo.emo:
			emolist.append(str(emo.emo[word]))
			text = text.replace(word," ")
	emores = ",".join(emolist)
	return text, emores

def slang_look_up(text):
	words = text.split()
	new_text = []
     
	for word in words:
		word_s = word.lower()
		if word_s in slangs.slangs:
			new_text.append(slangs.slangs[word_s])
		else:
			new_text.append(word)
	slanged = " ".join(new_text)
	return slanged

def appos_look_up(text):
	words = text.split()
	new_text = []

	for word in words:
		word_s = word.lower()
		if word_s in appos.appos:
			new_text.append(appos.appos[word_s])
		else:
			new_text.append(word)
	apposed = " ".join(new_text)
	return apposed

def improve_repeated(text):
	text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
	return text  
	
def clean_step1(text):
	text = decode_it(text)
	text = escape(text)
	text = appos_look_up(text)
	return text

def clean_step2(text):
	text = slang_look_up(text)
	text = improve_repeated(text)
	text, emo1 = emoticons_look_up(text)
	return text, emo1

''' Remove Special Characters '''
def clean_step3(text):
	removable = ['#','(',')','+','*','/',':',';','=','<','>','@','[',']','\\','^', '`', '{', '}', '|', '~','"']
	for x in removable:
		if x in text:
			text = text.replace(x," ")
	return text

''' Split the attached words '''
def clean_step4(line):
	if len(line.split()) == 1 and not line.isupper():
		lis = re.findall('[A-Z][^A-Z]*', line)
		if len(lis) == 0:
			nl = line
		else:
			nl = " ".join(re.findall('[A-Z][^A-Z]*', line))
	else:
		newd = []
		for word in line.split():
			if not word.isupper():
				lis = re.findall('[A-Z][^A-Z]*', word)
				if len(lis) == 0:
					newd.append(word)
				else:
					newd.append(" ".join(lis))
			else:
				newd.append(word)
		nl = " ".join(newd)
	return nl

def extra_rep(text):
	text = text.replace("??"," ? ").replace(".."," , ").replace("!!"," ! ").replace('""',' " ')
	text = re.sub(' +',' ',text)
	text = text.lstrip('"').lstrip('"')
	text = text.strip()
	if "!" in text and text[-1] != "!":
		text = text.replace("!"," , ")
	return text

''' Ginger Grammer Checker '''
''' Get URL '''
def get_ginger_url(text):
    API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
    scheme = "http"
    netloc = "services.gingersoftware.com"
    path = "/Ginger/correct/json/GingerTheText"
    params = ""
    query = urllib.urlencode([
        ("lang", "US"),
        ("clientVersion", "2.0"),
        ("apiKey", API_KEY),
        ("text", text)])
    fragment = ""
    return(urlparse.urlunparse((scheme, netloc, path, params, query, fragment)))

''' Connect with Ginger Api '''
def get_ginger_result(text):
    url = get_ginger_url(text)
    try:
        response = urllib.urlopen(url)
    except HTTPError as e:
            print("HTTP Error:", e.code)
            quit()
    except URLError as e:
            print("URL Error:", e.reason)
            quit()
    except IOError, (errno, strerror):
        print("I/O error (%s): %s" % (errno, strerror))
        quit
    try:
        result = json.loads(response.read().decode('utf-8'))
    except ValueError:
        print("Value Error: Invalid server response.")
        quit()
    return(result)

def grammetize(original_text):
    fixed_text = original_text
    results = get_ginger_result(original_text)
    color_gap = 0
    for result in results["LightGingerTheTextResult"]:
        if(result["Suggestions"]):
            from_index = result["From"] + color_gap
            to_index = result["To"] + 1 + color_gap
            suggest = result["Suggestions"][0]["Text"]
            orig = original_text[from_index:to_index]

            fixed_text = original_text[:from_index] + suggest + original_text[to_index:]

    return fixed_text

def clean_tweet(tweet):
	tweet1 = clean_step1(tweet)
	tweet2, emo1 = clean_step2(tweet1)
	tweet3 = clean_step3(tweet2)
	tweet4 = clean_step4(tweet3)
	tweet5 = extra_rep(tweet4)
	# if len(tweet5) < 600:
	# 	tweet6 = grammetize(tweet5)
	# else:
	# 	tweet6 = tweet5
	return str(tweet5), emo1