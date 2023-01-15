import pandas as pd
import requests
import json
import math

def getVideos(query, page=1):
    if page == 3: return []
    headers = { "Authorization": "563492ad6f917000010000018c59a1e684f44305a48003a16493cde7" }
    params = {
        "query": query,
        "orientation": "landscape",
        "size": "medium",
        "per_page": 100,
        "page": page
    }
    response = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['videos'] + getVideos(query, page+1)
        # jsonData = json.dumps(data, indent=4)
        # with open(f'{query}.json', 'w') as f:
        #     f.write(jsonData)
    else:
        print("Request failed with status code:", response.status_code)

def filterHD(urls):
    if urls['width'] == 1920:
        return True
    elif urls['width'] == 2560:
        return True
    elif urls['width'] == 3840:
        return True
    elif urls['width'] == 1280:
        return True
    return False

def removeNaNAndAppendList(df, columnName, l):
    column = df[columnName].tolist() 
    newColumn = list(filter(lambda row: type(row) == str, column))
    newColumn.extend(l)
    del df[columnName]
    df1 = pd.DataFrame({columnName: newColumn})
    df = pd.concat([df, df1], axis=1)
    return df


# write response to json
# with open('nature.json', 'r') as f:
# videos = json.loads(f.read())

if __name__ == '__main__':
    searchQueries = input('Search video topics: ').split(', ')
    for searchQuery in searchQueries:
        videos = getVideos(searchQuery)
        links = []
        for video in videos:
            HDVideos = list(filter(filterHD, video['video_files']))
            if len(HDVideos) == 0: continue
            links.append({
                'thumbnail': video['image'],
                'video': HDVideos[0]['link']
            })

        df = pd.read_csv('DB.csv')
        df = removeNaNAndAppendList(df, 'Videos', [link['video'] for link in links])
        df = removeNaNAndAppendList(df, 'Thumbnails', [link['thumbnail'] for link in links])
        df = removeNaNAndAppendList(df, 'Topic', [searchQuery]*len(links))

        df.to_csv('DB.csv', index=False)
        print('Data written to CSV file successfully')



'''
local workflow:
write video data to CSV file
write audios, title, description, subscribe text, Attribution, keywords to csv
upload csv to drive

kaggle workflow:
install packages code
mount the csv file from drive to kaggle
write video generation and upload code to kaggle
'''