import operator

import indicoio
import tweepy
import cogs.voice.tts as tts


def print_goodness_message(
        value,
        double_plus_good_text, good_text,
        ungood_text, double_plus_ungood_text):
    if value >= 0.8:
        # FIXME: Use a voice-synthesis function
        tts.speak(double_plus_good_text)
    elif 0.8 > value >= 0.4:
        tts.speak(good_text)
    elif 0.4 > value >= 0.2:
        tts.speak(ungood_text)
    elif 0.2 > value >= 0:
        tts.speak(double_plus_ungood_text)
    else:
        raise ValueError(
            "Value not in expected range: " + value)


def get_political_bias(biases):
    ranked_biases = sorted(biases.items(), key=operator.itemgetter(1), reverse=True)
    # [0]: first tuple in sorted list (with highest percentage)
    highest_bias = ranked_biases[0]
    return highest_bias


def length_ok(text):
    if len(text) > 140:
        print("Sorry, your tweet is too long: it's " +
              "{} characters. Can you make it shorter?".format(len(text)))
        return False
    else:
        return True


class Tweeter:
    def __init__(self, twitter_keys, indicoio_api_key):
        auth = tweepy.OAuthHandler(
            twitter_keys["consumer_key"],
            twitter_keys["consumer_secret"])
        auth.set_access_token(twitter_keys["access_key"], twitter_keys["access_secret"])
        self.api = tweepy.API(auth)

        indicoio.config.api_key = indicoio_api_key

    """
    Tweet a text, after checking for sentiment, engagement, and political 
    bias. Returns True on success; False on unsuccessfully sent tweet.
    """
    def tweet(self, text):
        if len(text) > 140:
            print("Sorry, but your tweet is more than 140 characters. Try a shorter one.")
            return

        tts.speak("Analyzing text...")
        analysis = indicoio.analyze_text(
            text,
            apis=['sentiment_hq', 'political', 'twitter_engagement'])

        tts.speak("Okay, let's take a look at the results.")

        print_goodness_message(
            analysis["sentiment_hq"],
            "Nice positivity!",
            "Emotion seems chill.",
            "That seems a little negative.",
            "That seems pretty negative.")
        if analysis["sentiment_hq"] <= 0.2:
            tts.speak("Hey, do you want to talk about this?")

        print_goodness_message(
            analysis["twitter_engagement"],
            "I suspect that this tweet'll be pretty popular.",
            "This'll probably be somewhat popular.",
            "I'm not sure if this'll appeal to many people.",
            "I think this one will be unpopular.")
        political_bias = get_political_bias(analysis["political"])
        if political_bias[1] >= 0.40:
            tts.speak("Seems that your tweet has a high {} bias.".format(political_bias[0]))

        if False:
            return False
        else:
            # Tweet it!
            self.api.update_status(text)
            tts.speak("And tweeted! Thanks.")
            return True
