from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

access_token = "2981137925-DCIVmb3Pf1WVZsXsYS3hANd0yQ1Q1Sncsrx446x"
access_token_secret = "qL3rRVkrtn8SQllQPpmY1Jj5MGwSNtqmCOfxKIRAIZivZ"
consumer_key = "Y8ZdIls5gqq2WgWNN4NiE5mSN"
consumer_secret = "PbvfvglaaOBVrwBMrQBCnIXzkxu1IHVJqyhb0uZiy6N19Ywib6"
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(languages=['en'],locations = [-74,40,-73,41])