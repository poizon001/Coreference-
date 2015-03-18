import json, requests, ast
from sentimentanalysis import sentiment, cleaner
import sentimentanalysis.FullNNP as fullname


def getData1(text, delimiter, bd, sentiment):
    url = 'http://localhost:8080/sae-1.0.0-BUILD-SNAPSHOT/analytics/analyse'
    json_data = {"sentence":text, "bd":bd, "sentiment":sentiment, "delimiter":delimiter}
    headers = {"Content-type": "application/json","Accept": "application/json"}
    jsonData = json.dumps(json_data)
    response = requests.post(url, headers=headers, data=jsonData)
    return response.json()

def make_tree(line):
	bd = getData1(line, bd=True, sentiment=False, delimiter="-")
	bd = "["+str(bd)+"]"
	bd = ast.literal_eval(bd)
	return bd



def filter_node(word):
	word = word.strip().replace("-> ","")
	word = str(word.rsplit("-",1)[0])
	return word

# text = "Barak Obama is the President of United States of America"
# text = "The Prime Minister of India visited Hydrabad House."
text = "The 21st Prime Ministers of India went to Parliament at 20 km per hour"


tree = make_tree(text)
sentiment.get_np(tree[0], tree[0])
sentiment.tree_parse(tree[0])