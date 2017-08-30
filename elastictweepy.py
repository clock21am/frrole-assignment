import tweepy  
import sys  
import json    
import csv
from textwrap import TextWrapper  
from datetime import datetime  
from elasticsearch import Elasticsearch
from tweepy.streaming import StreamListener


consumer_key="I0sQBHiLVYdZieIMfwHAyt3kR"  
consumer_secret="HWSM56rNkbsL27Ms3lfKPloQZM6Nd93Bv5F5fRAW3X2y7geLzg"
access_token="3317497801-I5JZxKOFLDp8VHhqTeUjL65FvnP1RJSr8F4ehyf"  
access_token_secret="iU5XrDGMhT35aUH8WVja4Y6iRrBtjwounM5j0z2jOgu8r"

es = Elasticsearch()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

es = Elasticsearch()

csvFile = open('result.csv', 'a')
csvWriter = csv.writer(csvFile)

class StreamListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            print '\n%s %s' % (status.author.screen_name, status.created_at)
            print status.text
            
            tweet = TextBlob(status.text)

            row=es.create(index="my-index", 
                      doc_type="test-type", 
                      body={ "author": status.author.screen_name,
                             "date": status.created_at,
                             "message": status.text,
                             "polarity": tweet.sentiment.polarity,
                             "subjectivity": tweet.sentiment.subjectivity }
                     )
            csvWriter.writerow(row)


        except Exception, e:
            pass

streamer = tweepy.Stream(auth=auth, listener=StreamListener())

#Fill with your own Keywords bellow
#terms = ['intel','#edison', '#galileo']

#myStreamListener = MyStreamListener()
#myStream = tweepy.Stream(auth = auth, listener=myStreamListener)
#myStream.filter(track=['Jon Snow'], async=True)

streamer.filter(track=['Jon Snow'], async=True)

