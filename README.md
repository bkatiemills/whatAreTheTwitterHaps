# whatAreTheTwitterHaps

Some hacky python to find out what's cool on twitter this week. `whatAreTheTwitterHaps(hashtag)` generates a text file listing tweets containing #`hashtag` and a non-picture link, sorted in decending order of number of retweets.

## setup
Uses the `python-twitter` wrapper for the twitter api:
```
sudo pip install python-twitter
```

Also, you'll need to set up an application, get its consumer key and consumer secret, and use it to generate an access token and access token secret, all of which can be done from their web UI, starting [here](https://apps.twitter.com/). 
