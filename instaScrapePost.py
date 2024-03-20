from datetime import datetime
import requests
import re

url = "https://instagram-scraper2.p.rapidapi.com/media_info_v2"
#Eventually we will have a large list of these
shortCodes = ['C4QmKmCLyDw','C4gX4Jwt1Nm', 'C4kg6rqKNQv','C4Jerk-NVCD']
for things in shortCodes:
	querystring = {"short_code": things}

	headers = {
		"X-RapidAPI-Key": "b914b9089amsh57d0a4103d72072p1b9c18jsna3a7dd730f95",
		"X-RapidAPI-Host": "instagram-scraper2.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)

	jsonData = response.json()
	print(response.json())

	# Extract the 'taken_at' value
	takenAtTimestamp = jsonData["items"][0]["taken_at"]
	# Convert to a datetime object
	postDate = datetime.fromtimestamp(takenAtTimestamp)
	formattedDate = postDate.strftime('%Y-%m-%d')

	likeCount = jsonData['items'][0]['like_count']
	description = jsonData['items'][0]['caption']['text']
	hashtags = re.findall(r'#\w+', description)

	with open('instagramData.txt', 'a', encoding='utf-8') as f:
		f.write(f"Hashtags: {str(hashtags)} Likes: {str(likeCount)} Date Added: {str(formattedDate)}\n")