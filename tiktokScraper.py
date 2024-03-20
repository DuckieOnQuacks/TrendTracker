import json
import requests
import re
from datetime import datetime

# Initialize a set to hold processed video IDs
processedVideoIds = set()

# Read existing video IDs from the file into the set to check for duplicates
with open('TrendTracker\TiktokData.json', 'r', encoding='utf-8') as f:
    for line in f:
        videoId = line.split(',')[0] 
        processedVideoIds.add(videoId) #.add doesnt do anything if item is already in the set

# Prepare the output file for appending new data
outputFile = open('TrendTracker\TiktokData.json', 'a', encoding='utf-8')
#Connect to api
url = "https://tiktok-api23.p.rapidapi.com/api/post/explore"
headers = {
    "X-RapidAPI-Key": "b914b9089amsh57d0a4103d72072p1b9c18jsna3a7dd730f95",
    "X-RapidAPI-Host": "tiktok-api23.p.rapidapi.com"
}

# Example of iterating, replace or modify according to your actual logic
querystring = {"categoryType": "119", "count": "50"}
response = requests.get(url, headers=headers, params=querystring)
jsonData = response.json()
lineToWrite = {}

for item in jsonData["itemList"]:
    videoId = item["id"]
    if videoId not in processedVideoIds:
        videoDetails = {
            "videoId": videoId,
            "likes": item["stats"]["diggCount"],
            "followerCount": item["authorStats"]["followerCount"],
            "hashtags": re.findall(r'#\w+', item['desc']),
            "createDate": datetime.fromtimestamp(item["createTime"]).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Convert the dictionary to a JSON string and write it to the file
        outputFile.write(json.dumps(videoDetails) + '\n')

# Close the file after writing
outputFile.close()

print("Data extraction and saving process completed.")
