import http.client
import json
import ast

api_url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com"
split_url = api_url.split('//')[1]
print(split_url)
api_key = "aAsE5_dgFglmHvU_6Mk_ZxwC-kYUKajbLSGgOiBrug2i"
#Question: make function that converts api_key to auth code so that can be used if api_key changes
conn = http.client.HTTPSConnection(split_url)
text = "I love apples! I do not like oranges"

payload_dict = {
  "text": text,
  "features": {
    "categories": {},
    "keywords": {}
  }
}
payload = json.dumps(payload_dict)

headers = {
    'Content-Type': "application/json",
    'Authorization': "Basic YXBpa2V5OmFBc0U1X2RnRmdsbUh2VV82TWtfWnh3Qy1rWVVLYWpiTFNHZ09pQnJ1ZzJp"
    }

conn.request("POST", "/instances/052cc707-bf94-45d1-8033-5b3623b0f35d/v1/analyze?version=2019-07-12", payload, headers)

res = conn.getresponse()

data = res.read().decode("utf-8")
#print(data)
json_data = ast.literal_eval(data)

#print(data.decode("utf-8"))
#want to produce a list of keywords (text) and list of categories (label) in order of appearance
keywords = []
for i in json_data["keywords"]:
    keywords.append(i['text'])
print(keywords)

categories = []
for i in json_data["categories"]:
    categories.append(i['label'])
print(categories)