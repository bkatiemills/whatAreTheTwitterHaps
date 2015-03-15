import twitter
import datetime
import dateutil.parser

# Consumer keys and access tokens, used for OAuth
consumer_key = 'kittens'
consumer_secret = 'rainbows'
access_token = 'unicorns'
access_token_secret = 'sunshine'

api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token,
                      access_token_secret)

def nextPage(search, max):
    '''
    fetch 100 tweets from <search>, prior to tweet with id=<max>
    '''
    page =  api.GetSearch(term=search, max_id=max, count=100)
    return page

def olderThan(tweet, days):
    '''
    is <tweet> older than <days> old?
    '''
    tweetDate = dateutil.parser.parse(tweet.created_at).replace(tzinfo=None)
    cutoff = dateutil.parser.parse(str(datetime.date.today() - datetime.timedelta(days) ) )
    return tweetDate < cutoff

def linksOnly(tweets):
    '''
    takes a list of tweets, and returns the subset containing links that aren't twitpics
    '''
    linkTweets = []
    for tweet in tweets:
        if (len(tweet.media) > 0):
            if(tweet.media[0]['type'] == 'photo'):
                continue

        if (tweet.text.find('http')>-1):
            linkTweets.append(tweet)

    return linkTweets

def whatAreTheTwitterHaps(hashtag):
    '''
    search for tweets from the last 7 days containing #<hashtag>
    dump any that don't have an interesting link
    sort what's left by number of retweets
    save in a file <hashtag>YYYY-MM-DD, where the date is today's,
    with tweet id, text, no. retweets and timestamp separated by ' ^^^ '
    '''

    f = open(hashtag+str(datetime.date.today()), 'w')

    rawTweets = api.GetSearch(term='#'+hashtag+' +exclude:retweets', count=100)

    limiter=0 #don't spam the api
    while ( (not olderThan(rawTweets[-1], 7)) and limiter<10 ):
        oldestID = rawTweets[-1].id
        more = nextPage('#'+hashtag+' +exclude:retweets', oldestID)
        if (len(more)==0):
            break;
        rawTweets = rawTweets + more
        limiter = limiter+1

    linkedTweets = linksOnly(rawTweets)

    sortedTweets = sorted(linkedTweets, key=lambda thisone: thisone.retweet_count, reverse=True)

    for tweet in sortedTweets:
        s =  str(tweet.id) + ' ^^^ ' + tweet.text.replace('\n', '') + ' ^^^ ' + str(tweet.retweet_count) + ' ^^^ ' + '"' + tweet.created_at + '"' + '\n'
        s = s.encode('ascii', 'ignore')
        f.write(s)


whatAreTheTwitterHaps('openscience')
