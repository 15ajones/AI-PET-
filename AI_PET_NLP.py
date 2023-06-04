import http.client
import json
import ast
import base64
import re

def hasTime(sentence):
    # Regular expression pattern for time
    timeKeywords = ["morning", "afternoon", "evening", "night"]
    timePattern = r"\b(?:{})\b".format("|".join(timeKeywords))
    hourPattern = r"\b\d{1,2}(?: o'clock| a.m| p.m)\b"

    timeKeywordMatches = re.findall(timePattern, sentence, re.IGNORECASE)
    hourMatches = re.findall(hourPattern, sentence, re.IGNORECASE)

    matches = timeKeywordMatches + hourMatches #concatenates list

    # Find the starting index of each match in the sentence
    indices = [sentence.lower().index(match.lower()) for match in matches]
    #for each match in matches, we get the index of it in the sentence
    # Sort the matches based on their starting indices
    sorted_matches = [match for _, match in sorted(zip(indices, matches))]

    return sorted_matches
    
def hasDate(sentence):
    # Check for specific date keywords
    dateKeywords = ["today", "tomorrow", "yesterday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "next week", "last week"] #what about next week saturday/next tuesday -> must find ways to resolve this
    datePattern = r"\b(?:{})\b".format("|".join(dateKeywords))
    
    return re.findall(datePattern, sentence, re.IGNORECASE)

def getStrongestEmotion(emotionList):
    newList = dict(sorted(emotionList.items(), key = lambda x:x[1], reverse = True))
    firstValue = list(newList.items())[0][0]
    return firstValue

def categoriseText(text):#redo with corrent authentification process
    api_url1 = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/021acc9f-fa3e-43da-a7f3-6ea134e47856"
    split_url = api_url1.split('//')[1]
    api_url = split_url.split('com')[0] + "com"
    second_url= split_url.split('com')[1]
    api_key = "9yLrG_r0CsOBJ9nzEDGCvgNUTk315WH-NUoHDnzFcQIM"

    conn = http.client.HTTPSConnection(api_url)


    payload_dict = {
      "text": text,
      "features": {
        "categories": {},
        "keywords": {
            "emotion": True,#might have to change 'but' to seperate sentences
            }
      }
    }
    payload = json.dumps(payload_dict)

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic YXBpa2V5Ojl5THJHX3IwQ3NPQko5bnpFREdDdmdOVVRrMzE1V0gtTlVvSERuekZjUUlN"
        }

    conn.request("POST", second_url + "/v1/analyze?version=2019-07-12", payload, headers)

    res = conn.getresponse()

    data = res.read().decode("utf-8")
   #print(data)
    json_data = ast.literal_eval(data)
    keywords = []
    emotions = []
    try:
        for i in json_data["keywords"]:
            keywords.append(i['text'])
            emotions.append(i['emotion'])
    except:
        return ["conv"]#no keywords
    print(keywords)
    #print(emotions)

    categories = []
    for i in json_data["categories"]:
        categories.append(i['label'])
    #print(categories)
    state = ""
    planningKeywords = ["arrange", "schedule", "plan"]
    checkingKeywords = ["check"]
    user_input = text.lower()  # Convert input to lowercase for case-insensitive matching
    textList = text.split(" ")
    for keyword in planningKeywords:
        if keyword in user_input:
            print(user_input)
            if any(t == "What" for t in textList) or any(t == "What's" for t in textList):
                print("checking")
                state = "checking"
            else:
                if (keyword in keywords):
                    print("checking")
                    state = "checking"
                else:
                    print("planning")
                    state = "planning"

    for keyword in checkingKeywords:
        if keyword in user_input:
            print("checking")
            state = "checking"
    
    #dateLists = ["today", "tomorrow", "next week", "last week", "yesterday", "time", "calendar"]#also include full list of datetimes
    activities = []
    if state == "checking":
        time = hasTime(text.lower())
        date = hasDate(text.lower())
        #if no datetime, prompt to ask for datetime?
        return ["check"] , date, time #check with Anthony if ok format
    elif state == "planning":
        print(keywords)
        time = hasTime(text.lower())
        date = hasDate(text.lower())
        print("time ", time)
        for t in keywords: 
            if t != "calendar":#test to find useless keywords/or will this be for Anthony to do
                if len(hasTime(t)) < 1:
                    activities.append(t)
                    print(t)
                
        return ["plan"], date,time,activities

    

    elif any(t == "podcast" for t in keywords) or any(t == "podcasts" for t in keywords):
        
        print ("podcast function")
        interest = []
        i = 0
        for t in keywords:
            if t != "podcast" and t != "podcasts":#need to find way to eliminate any word with this in it
                if getStrongestEmotion(emotions[i]) == 'joy':#since other options = fear, disgust, anger, sadness
                    interest.append(t)
            i += 1
        print("interests: ", interest)
        return ["p", interest ]#first letter = what type, followed by topics to search
    elif any(t == "emails" for t in keywords) or any(t == "email" for t in keywords):
        print ("email function")#for now assuming its just receive not send e.g. do we have any new emails?
        return ["e"]
    elif any(t == "weather" for t in keywords):
        print ("weather function")
        return ["w"]
    elif any(t == "news" for t in keywords):
        print ("news function")
        return ["n"]
    elif any (t == "music" for t in keywords) or any(t == "song" for t in keywords) or any(t == "songs" for t in keywords):
        print ("music function")
        genre = []#or artist
        i = 0
        for t in keywords:
            if t != "music" and t != "song" and t != "songs":
                if getStrongestEmotion(emotions[i]) == 'joy':
                    genre.append(t)
            i += 1
        print(genre)
        return ["m", genre]
    else:
        print ("conversation")
        return ["conv"]
    


#print(categoriseText("I want to watch a movie at 2 a.m tomorrow. I also need to go to school on Friday afternoon. Please schedule this in my calendar"))
#print(categoriseText("What is scheduled in my calendar for thursday at 2 p.m?"))
print(categoriseText("I want to listen to a podcast. I like self improvement. What do you recommend?"))
#in user guide -> user must say both date and time/especially when multiple activities: if not/if the length of dates doesn't match length of activities/times prompt user?
#will it try to find what time it is free?
