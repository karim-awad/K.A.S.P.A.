from Kaspa.modules.abstract_modules.abstractSubmodule import AbstractSubmodule


class RedditModuleEn(AbstractSubmodule):

    module_name = "Reddit"

    language = "en"

    key_regexes = dict()

    def __init__(self):
        self.key_regexes = {'(?i).*?(?=tell)+.+?(?=joke)+.': self.action_joke,
                       '(?i).*?(?=tell)+.+?(?=thought)+.': self.action_thought,
                       '(?i).*?(?=tell)+.+?(?=fact)+.': self.action_fact}

    def action_joke(self, query):
        communicator = query.get_communicator()
        submission = self.main_module.get_random("jokes", 100)
        while len(submission.selftext) > 500:  # make sure the jokes aren't too long. not a high performance solution
            submission = self.main_module.get_random("jokes", 100)
        joke = submission.title + "\n" + submission.selftext
        communicator.say(joke)

    def action_thought(self, query):
        communicator = query.get_communicator()
        submission = self.main_module.get_random("showerthoughts", 100)
        thought = submission.title + "\n" + submission.selftext
        communicator.say(thought)

    def action_fact(self, query):
        communicator = query.get_communicator()
        fact = self.main_module.get_random("todayilearned", 20).title
        answer = "Today I learned " + fact[4:]
        communicator.say(answer)