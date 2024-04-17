import json
import requests
import re
from datetime import datetime

# Initialize a set to hold processed video IDs
processedVideoIds = set()

def scrapeData():
    # Read existing video IDs from the file into the set to check for duplicates
    with open('TiktokData.json', 'r', encoding='utf-8') as f:
        for line in f:
            videoId = line.split(',')[0] 
            processedVideoIds.add(videoId) #.add doesnt do anything if item is already in the set
            print(videoId)

    # Prepare the output file for appending new data
    outputFile = open('TiktokData.json', 'a', encoding='utf-8')
    #Connect to api
    url = "https://tiktok-api23.p.rapidapi.com/api/post/trending"
    headers = {
        "X-RapidAPI-Key": "b914b9089amsh57d0a4103d72072p1b9c18jsna3a7dd730f95",
        "X-RapidAPI-Host": "tiktok-api23.p.rapidapi.com"
    }

    querystring = {"count": "30"}
    response = requests.get(url, headers=headers, params=querystring)
    jsonData = response.json()

    for item in jsonData["itemList"]:
        videoId = item["id"]
        if videoId not in processedVideoIds:
            hashtags = re.findall(r'#\w+', item['desc'])  # Extract hashtags from description.
            if hashtags and all(re.match(r'^#[A-Za-z0-9_]+$', tag) for tag in hashtags):
                videoDetails = {
                    "videoId": videoId,
                    "likes": item["stats"]["diggCount"],
                    "followerCount": item["authorStats"]["followerCount"],
                    "hashtags": hashtags,
                    "createDate": datetime.fromtimestamp(item["createTime"]).strftime('%Y-%m-%d %H:%M:%S')
                }
                outputFile.write(json.dumps(videoDetails) + '\n')

    print("Data extraction and saving process completed.")

for i in range(0,8):
    scrapeData()