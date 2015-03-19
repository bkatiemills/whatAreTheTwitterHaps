import twitter
import datetime
import dateutil.parser
import ast

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

def whatAreTheTwitterHaps(text, maxCalls=10, maxDays=7):
    '''
    search for unique tweets containing <text>
    give up once we start finding tweets <maxDays> old
    don't make more than <maxCalls> to the API
    '''

    tweets = api.GetSearch(term=text+' +exclude:retweets', count=100)

    limiter=0 #don't spam the api
    while ( (not olderThan(tweets[-1], maxDays)) and limiter<maxCalls ):
        oldestID = tweets[-1].id
        more = nextPage(text+' +exclude:retweets', oldestID)
        if (len(more)==0):
            break;
        tweets = tweets + more
        limiter = limiter+1

    return tweets

def sortTweets(tweets, key):
    '''
    sorts <tweets> by <key>, and returns the sorted list
    watch out! I'm a horrible person, and eval'ed this
    '''
    hackySort = 'sorted(tweets, key=lambda thisone: thisone.'+key+', reverse=True)'
    sortedTweets = eval(hackySort)

    return sortedTweets

def logTweets(tweets, prefix='tweets'):
    '''
    save <tweets> in a file <prefix>.YYYY-MM-DD, where the date is today's,
    with tweet id, text, no. retweets and timestamp separated by ' ^^^ '
    '''
    f = open(prefix+'.'+str(datetime.date.today()), 'w')

    for tweet in tweets:
        s =  str(tweet.id) + ' ^^^ ' + tweet.text.replace('\n', '') + ' ^^^ ' + str(tweet.retweet_count) + ' ^^^ ' + '"' + tweet.created_at + '"' + '\n'
        s = s.encode('ascii', 'ignore')
        f.write(s)

tweets = whatAreTheTwitterHaps('#openscience')
interestingT = linksOnly(tweets)
sortedT = sortTweets(interestingT, 'retweet_count')
logTweets(sortedT)
