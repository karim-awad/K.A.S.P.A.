from Kaspa.modules.abstract_modules.abstractModule import AbstractModule
from Kaspa.modules.extension_modules.reddit_module.redditModuleEn import RedditModuleEn
from Kaspa.config import Config

import praw
import random


class RedditModuleMain(AbstractModule):

    config_parameters = {"client_id": "At first you have to create a new Application: \n"
                                      "https://www.reddit.com/prefs/apps/\n After doing so, you can find your"
                                      "client_id on the same page.",
                         "client_secret": "This secret key can also be found on there.",
                         "user_agent": "This is the name of your app displayed on yet again the same page."}

    module_name = "Reddit"

    reddit = None

    def __init__(self):
        super(RedditModuleMain, self).__init__()
        # Found no use for a german module at the moment
        self.add_submodule(RedditModuleEn())

    def configure(self):
        config = Config.get_instance()
        client_id = config.get('reddit', 'client_id')
        client_secret = config.get('reddit', 'client_secret')
        user_agent = config.get('reddit', 'user_agent')

        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    def get_burst(self, subreddit, limit):
        return list(self.reddit.subreddit(subreddit).top(limit=limit, time_filter='day'))

    def get_random(self, subreddit, limit):
        posts = list(self.reddit.subreddit(subreddit).hot(limit=limit))
        return random.choice(posts)

    def get_top(self, subreddit):
        posts = list(self.reddit.subreddit(subreddit).top(limit=1, time_filter='day'))
        return posts[0]

    # def briefing_action(self, query):
    #     communicator = query.get_communicator()
    #     submission = self.get_random("showerthoughts", 100)
    #     thought = "Here is a random thought for you: " + submission.title + "\n" + submission.selftext
    #     communicator.say(thought)
