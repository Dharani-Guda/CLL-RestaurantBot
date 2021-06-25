import requests
import random

def check_location(loc):
    loc=loc[0].upper()+loc[1:].lower()
    url = "https://developers.zomato.com/api/v2.1/locations?query="+loc
    payload={}
    headers = {
    'user-key': 'dc4f13f34b2754f1b044d01e36008001',
    'Cookie': 'zl=en; fbtrack=4ab6df8721591043ea5d457ed1b3a266; AWSALBTG=G5FkFTw+4mX6npjwqrbdya76NwGh1xjt59uV2V+LuvXUcmUmEBNxyPlqi1OFgxxi4K4Cr2FZ5fjYvmVNHr20HadMUZZ1MdZUcf6Gnk+ICSGQvoHCfYlYmYiFUb5+7kfImu7TeleV1x4pP3JjEDMeC6+Zb00TOyE72FkJa2730hdTZYVq92k=; AWSALBTGCORS=G5FkFTw+4mX6npjwqrbdya76NwGh1xjt59uV2V+LuvXUcmUmEBNxyPlqi1OFgxxi4K4Cr2FZ5fjYvmVNHr20HadMUZZ1MdZUcf6Gnk+ICSGQvoHCfYlYmYiFUb5+7kfImu7TeleV1x4pP3JjEDMeC6+Zb00TOyE72FkJa2730hdTZYVq92k=; csrf=2969c9d7bf16b0eea6443d567309bc7f; fbcity=11434'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result=response.json()
    if(len(result["location_suggestions"])!=0):
        entity_id=result["location_suggestions"][0]["entity_id"]
        entity_type=result["location_suggestions"][0]["entity_type"]
        return entity_id,entity_type
    else:
        return None,None

def check_cuisine(city_id,cuisine):
    cuisine=cuisine[0].upper()+cuisine[1:].lower()
    url = "https://developers.zomato.com/api/v2.1/cuisines?city_id="+str(city_id)
    payload={}
    headers = {
    'user-key': 'dc4f13f34b2754f1b044d01e36008001',
    'Cookie': 'zl=en; fbtrack=4ab6df8721591043ea5d457ed1b3a266; fbcity=11434; AWSALBTG=g9o9mHj+puqAN+cLUpHaLg0xILc1R2mT3NFV8SNRrp+ISk9tj5kbdmZXCIM2pikiem3jv5Usf5r6jeod2ogfr9qKdBfRsBF/egwrDpBwRafUzA/Mv2OqGPJcw36a/1jzvr2yuFUTzt6fpssCW4kgLEctp4ZM5UwFLKTdaCC1sfFXNV90WV4=; AWSALBTGCORS=g9o9mHj+puqAN+cLUpHaLg0xILc1R2mT3NFV8SNRrp+ISk9tj5kbdmZXCIM2pikiem3jv5Usf5r6jeod2ogfr9qKdBfRsBF/egwrDpBwRafUzA/Mv2OqGPJcw36a/1jzvr2yuFUTzt6fpssCW4kgLEctp4ZM5UwFLKTdaCC1sfFXNV90WV4=; csrf=804ff4a8a933213b83e9eccd71c0a3c8'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result=response.json()
    _cuisine=result["cuisines"]
    cuisine_id=[]
    cuisine_name=[]
    for i in _cuisine:
        cuisine_id.append(i['cuisine']['cuisine_id'])
        cuisine_name.append(i['cuisine']['cuisine_name'])
    res = {cuisine_name[i]: cuisine_id[i] for i in range(len(cuisine_name))}
    if(cuisine in cuisine_name):
        return res[cuisine]
    else:
        return None

def find_cuisine(entity_id,entity_type):
    url = "https://developers.zomato.com/api/v2.1/location_details?entity_id="+str(entity_id)+"&entity_type="+entity_type

    payload={}
    headers = {
    'user-key': 'dc4f13f34b2754f1b044d01e36008001',
    'Cookie': 'zl=en; fbtrack=4ab6df8721591043ea5d457ed1b3a266; AWSALBTG=OrSP8j41YTfar1sXdv59MBAoQ29ChDRXysavGW8KVb25szRFOlzTAQ9w7/XK4k3EYw3iFORbs/8tHZ0UW1go2W84hkAcgdU2HOk4/48KJ7Z4BXwTyxrNQPfi5SiMnX2fIKI7ajXGLUfXmXAk1ClPYW6XwkN2B033wFMzgWtmNtGYiD7WwhM=; AWSALBTGCORS=OrSP8j41YTfar1sXdv59MBAoQ29ChDRXysavGW8KVb25szRFOlzTAQ9w7/XK4k3EYw3iFORbs/8tHZ0UW1go2W84hkAcgdU2HOk4/48KJ7Z4BXwTyxrNQPfi5SiMnX2fIKI7ajXGLUfXmXAk1ClPYW6XwkN2B033wFMzgWtmNtGYiD7WwhM=; csrf=e0772b51788e01bed87602470538b3b1; fbcity=7'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    result=response.json()
    top_cuisine=result["top_cuisines"]
    cuisine=random.choice(top_cuisine)
    return cuisine

def restaurant_search(entity_id,entity_type,cuisine,radius,establishment,category):
    url = url = "https://developers.zomato.com/api/v2.1/search?count=5&cuisine="+cuisine+"&entity_id="+str(entity_id)+"&entity_type="+entity_type+"&radius="+str(radius)+"&establishment_type="+establishment+"&category="+category
    payload={}
    headers = {
    'user-key': 'dc4f13f34b2754f1b044d01e36008001',
    'Cookie': 'zl=en; fbtrack=4ab6df8721591043ea5d457ed1b3a266; fbcity=7; AWSALBTG=Hwq4nZave9ZDboNkF0dmsrS07aqijF97p7O7T4JYRJXFpVDDwklJF9coTFWfMq41jyF96iSRXewiJugCx4ntk9FWfiZc8EelPDe+gABYD/hUFeHjL05j6OKCuRnfozCNVzQDQ7vEk4PSEYupMlwKBXXHIKFMmjwYFb1P267fuGUW4EoyBck=; AWSALBTGCORS=Hwq4nZave9ZDboNkF0dmsrS07aqijF97p7O7T4JYRJXFpVDDwklJF9coTFWfMq41jyF96iSRXewiJugCx4ntk9FWfiZc8EelPDe+gABYD/hUFeHjL05j6OKCuRnfozCNVzQDQ7vEk4PSEYupMlwKBXXHIKFMmjwYFb1P267fuGUW4EoyBck=; csrf=541d465da19a3208e60d7d6b8a04dc78'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    result=response.json()
    restaurant=result["restaurants"]
    restaurants=[]
    c=0
    for i in restaurant:
        if(i["restaurant"]["name"] not in restaurants and c!=5):
            restaurants.append("Restaurant : "+i["restaurant"]["name"]+" ; Address : "
                            +i["restaurant"]["location"]["address"]+" ; Phone number : "
                            +i["restaurant"]["phone_numbers"]+" ; User ratings : "
                            +i["restaurant"]["user_rating"]["aggregate_rating"])
            c+=1
    return restaurants

