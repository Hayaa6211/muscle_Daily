import os
import tweepy
from datetime import datetime,timezone,date

data = []
class Tweet:
    def __init__(self):
        self.api_key = os.getenv("API_Key")
        self.api_secret = os.getenv("API_Key_Secret")
        self.access_token = os.getenv("Access_Token")
        self.access_secret = os.getenv("Access_Token_Secret")
        self.count = 0
        self.tweet = []

        self.today = date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day

        self.auth = tweepy.OAuthHandler(self.api_key,self.api_secret)
        self.auth.set_access_token(self.access_token,self.access_secret)
        self.api = tweepy.API(self.auth)
    
    def get_Tweet(self):
        results = self.api.user_timeline(screen_name="amazons_iwata",include_rts = False)
        return results
    
    def check_date(self,tweets:list,startDate,endDate):
        for tweet in tweets:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                if tweet.text[0] == '@': continue
                self.tweet.append(tweet)
        
        while (tweets[-1].created_at > startDate):
            tweets = self.api.user_timeline(screen_name = "amazons_iwata",max_id = tweets[-1].id,include_rts = False)
            for tweet in tweets:
                if tweet.created_at < endDate and tweet.created_at > startDate:
                    if tweet.text[0] == '@': continue
                    self.tweet.append(tweet)
        
        return self.tweet
    
    def count_tweet(self,tweets:list):
        return len(tweets)

    def make_Tweet(self,year=None,month=None,day=None,count=0):
        if year == None: year = self.year
        if month== None: month= self.month
        if day ==  None: day  = self.day
        text = f"#はやあ毎日筋トレ\n\n{year}年{month}月{day}日のツイート数は{count}だったので今日の筋トレ回数は{count*10}回です．ふぁいてぃん💪💪💪"
        return text

    def Do_Tweet(self,text:str,pic:str = None):
        if not pic == None:
            self.api.update_status_with_media(status=text,filename=pic)
        else:
            self.api.update_status(status=text)

class Date:
    def __init__(self):
        self.today = date.today()
        self.year = self.today.year
        self.month = self.today.month
        self.day = self.today.day
    
    def set_Date(self,year=None,month=None,day=None,end=False):
        if year == None: year = self.year
        if month== None: month= self.month
        if day ==  None: day  = self.day
        if not end: day -= 1
        new_date = datetime(year,month,day,21,0,0,tzinfo=timezone.utc)
        return new_date
    
class Debug:
    def __init__(self):
        pass

    def check_tweet_text(self,tweets):
        return [tweet.text for tweet in tweets]
    
    def check_tweet_count(self,tweets):
        return len(tweets)
    
    def check_tweet_time(self,tweets):
        return [tweet.created_at for tweet in tweets]

def main():
    t = Tweet()
    date = Date()
    debug = Debug()

    startDate = date.set_Date()
    endDate = date.set_Date(end=True)

    tweets = t.get_Tweet()
    tweets = t.check_date(tweets,startDate,endDate)
    count = t.count_tweet(tweets)
    text = t.make_Tweet(count=count)
    t.Do_Tweet(text)

if __name__ == "__main__":
    main()