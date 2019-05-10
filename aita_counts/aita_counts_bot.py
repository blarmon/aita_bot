import re
from collections import defaultdict
import threading
from queue import Queue

import config

reddit = config.reddit_config
subreddit = reddit.subreddit('AmITheAsshole')

# TODO! maybe write successful comments out to a file with some metadata.  could be fun to have the data in json format down the line or something.
# TODO.  grab the most upvoted comment for each type of vote and link to it.  that's good stuff.
# TODO clean up variable shadowing
# TODO error handling

def generate_counts(submission_id):
    submission = reddit.submission(id=submission_id)
    aita_dict = defaultdict(int)

    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        matcher = aita_regex.search(comment.body)
        if matcher:
            aita_dict[matcher.group(1)] += 1

    total_votes_all = sum([v for v in aita_dict.values()])
    bot_comment = []

    for k, v in aita_dict.items():
        bot_comment.append(f"{k} has {str((v/total_votes_all)*100).split('.')[0]}% of all of the comments with votes in"
                  f" this submisson. ({v}/{total_votes_all} total comments)" + "\n\n")

    bot_comment.append(
        "\n\n^I ^am ^the ^AITA ^bot!  ^Post ^'!aita_bot' ^in ^any ^AmITheAsshole ^submission ^and ^I'll ^reply ^to ^your"
        " ^comment ^with ^counts ^and ^percentages ^of ^how ^users ^voted ^in ^this ^thread.")
    bot_comment.append('\n\n')
    bot_comment.append("^^Feel ^^free ^^to ^^message ^^the ^^creator, ^^/u/blarmon_kek ^^with ^^any ^^questions,"
                       " ^^concerns, ^^or ^^suggestions!")

    return ''.join(bot_comment)


def threader():
    while True:
        if not q.empty():
            comment = q.get()
            comment.reply(generate_counts(comment.submission.id))
            q.task_done()


if __name__ == '__main__':

    key_phrase = '!aita\_bot'
    q = Queue()
    aita_regex = re.compile(r'(YTA|NTA|ESH|NAH|INFO)')

    for _ in range(5):
        t = threading.Thread(target=threader)
        t.daemon = False
        t.start()

    while True:
        for comment in subreddit.stream.comments(skip_existing=True):
            if key_phrase in comment.body:
                q.put(comment)
