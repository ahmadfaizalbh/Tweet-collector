#!/usr/bin/env python
import sys
import rfc822
import time
import json
from urllib import urlopen, urlencode
from tweetconnect import *
from auth_and_Secret import TweetOuth

def getUserTweet(screen_name,**kwargs):
    """
    Get tweets from specific user time line
    getUserTweet(screen_name,count=100,since_id='twitter id',max_id='twitter id')
    """
    args = dict(count=100, trim_user=1, screen_name=screen_name)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url) 
    return json.loads(user_timeline)

def getSearchTweet(Search_key,**kwargs):
    """
    Search twiiter with with specified key
    getSearchTweet(Search_key,,count=100,since_id='twitter id',max_id='twitter id')
    """
    args = dict(count=100, q=Search_key)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/search/tweets.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url) 
    return json.loads(user_timeline)

def getFriends(screen_name):
    """
    Get User details of all Friends
    getFriends(screen_name)
    """
    FollowingList=[]
    follow=TweetOuth.tweet_req('https://api.twitter.com/1.1/friends/ids.json?'+urlencode_utf8({'cursor':-1,'screen_name':screen_name,'count':5000}))
    result=json.loads(follow)
    follow_ids=result[u'ids']
    while result[u'next_cursor']:
        follow=TweetOuth.tweet_req('https://api.twitter.com/1.1/friends/ids.json?'+urlencode_utf8({'cursor':result[u'next_cursor'],'screen_name':screen_name,'count':5000}))
        result=json.loads(follow)
        follow_ids+=result[u'ids']
    follow_list=follow_ids
    while follow_list:
        req_list=str(follow_list[0])
        for i in follow_list[1:100]:
            req_list+=','+str(i)
        lookup=TweetOuth.tweet_req('https://api.twitter.com/1.1/users/lookup.json?user_id='+req_list)
        lookup_result=json.loads(lookup)
        for i in lookup_result:
            FollowingList.append([str(i[u'id']),i[u'name'],i[u'screen_name'],str(i[u'followers_count']),str(i[u'friends_count'])])
        follow_list=follow_list[100:]
    return FollowingList

def getFollower(screen_name):
    """
    Get User details of all Follower
    getFollower(screen_name)
    """
    FollowersList=[]
    follow=TweetOuth.tweet_req('https://api.twitter.com/1.1/followers/ids.json?'+urlencode_utf8({'cursor':-1,'screen_name':screen_name,'count':5000}))
    result=json.loads(follow)
    follow_ids=result[u'ids']
    while result[u'next_cursor']:
        follow=TweetOuth.tweet_req('https://api.twitter.com/1.1/followers/ids.json?'+urlencode_utf8({'cursor':result[u'next_cursor'],'screen_name':screen_name,'count':5000}))
        result=json.loads(follow)
        follow_ids+=result[u'ids']
    follow_list=follow_ids
    while follow_list:
        req_list=str(follow_list[0])
        for i in follow_list[1:100]:
            req_list+=','+str(i)
        lookup=TweetOuth.tweet_req('https://api.twitter.com/1.1/users/lookup.json?user_id='+req_list)
        lookup_result=json.loads(lookup)
        for i in lookup_result:
            FollowersList.append([str(i[u'id']),i[u'name'],i[u'screen_name'],str(i[u'followers_count']),str(i[u'friends_count'])])
        follow_list=follow_list[100:]
    return FollowersList

def getTweetFromList(screen_name,slug,**kwargs):
    """
    Get tweet from a specific twitter list
    getTweetFromList(screen_name,slug,count=100,since_id='twitter id',max_id='twitter id')
    """
    args = dict(count=180, slug=slug,owner_screen_name=screan_name)
    args.update(**kwargs)
    url = 'https://api.twitter.com/1.1/lists/statuses.json?' + urlencode(args)
    user_timeline = TweetOuth.tweet_req(url) 
    return json.loads(user_timeline)
