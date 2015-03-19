# whatAreTheTwitterHaps

Some hacky python to find out what's cool on twitter this week. `whatAreTheTwitterHaps(text)` pulls down a list of tweets containing `text`; some other helper functions are available to tidy up what gets pulled down.

## setup
Uses the `python-twitter` wrapper for the twitter api:
```
sudo pip install python-twitter
```

Also, you'll need to set up an application, get its consumer key and consumer secret, and use it to generate an access token and access token secret, all of which can be done from their web UI, starting [here](https://apps.twitter.com/). 
