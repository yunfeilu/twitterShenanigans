import json
import re
import unicodedata

tweets_data_path = 'twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")
doc = open('doc.txt','w')
temp_str = ""
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

for item in tweets_data:
    if 'limit' in item:
        continue
    temp = item
    total_text = ""
    quoted_text = ""
    hashtag_text = ""

    if 'extended_tweet' in temp:
        total_text += temp['extended_tweet']['full_text']
        if 'text' in temp['extended_tweet']['entities']['hashtags']:
            hashtag_text += ' '.join(temp['extended_tweet']['entities']['hashtags']['text'])
    else:
        total_text += temp['text']
        if 'text' in temp['entities']['hashtags']:
            hashtag_text += ' '.join(temp['entities']['hashtags']['text'])

    total_text += ' '
    hashtag_text += ' '


    while 'quoted_status' in temp:
        temp = temp['quoted_status']
        if 'extended_tweet' in temp:
            total_text += temp['extended_tweet']['full_text']
            if 'text' in temp['extended_tweet']['entities']['hashtags']:
                hashtag_text += ' '.join(temp['extended_tweet']['entities']['hashtags']['text'])
        else:
            total_text += temp['text']
            if 'text' in temp['entities']['hashtags']:
                hashtag_text += ' '.join(temp['entities']['hashtags']['text'])

        total_text += ' '
        hashtag_text += ' '
    text = total_text + hashtag_text
    result = re.sub(r"http\S+", "", text)
    result = result.encode('ascii', errors='replace')
    temp_str += result.decode() + "\n"


doc.write("".join([s for s in temp_str.strip().splitlines(True) if s.strip()]))
