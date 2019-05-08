import re
from collections import defaultdict
import threading

import config

reddit = config.reddit_config

subreddit = reddit.subreddit('AmItheAsshole')


def generate_counts(submission_id):
    submission = reddit.submission(id=submission_id)

    aita_regex = re.compile(r'(YTA|NTA|ESH|NAH|INFO)')
    bot_comment = []


    # all comments
    aita_dict_all = defaultdict(int)

    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        matcher = aita_regex.search(comment.body)
        if matcher:
            aita_dict_all[matcher.group(1)] += 1

    total_votes_all = sum([v for v in aita_dict_all.values()])

    for k, v in aita_dict_all.items():
        bot_comment.append(f"{k} has {str((v/total_votes_all)*100).split('.')[0]}% of all of the comments with votes in"
                  f" this submisson. ({v}/{total_votes_all} total comments)" + "\n\n")

    bot_comment.append(
        "\n\n^I ^am ^the ^AITA ^bot!  ^Post ^'!aita_bot' ^in ^any ^AmITheAsshole ^submission ^and ^I'll ^reply ^to ^your ^comment ^with ^counts ^and ^percentages"
        " ^of ^how ^users ^voted ^in ^this ^thread.")
    bot_comment.append('\n\n')
    bot_comment.append("^^Feel ^^free ^^to ^^message ^^the ^^creator, ^^/u/blarmon_kek ^^with ^^any ^^questions, ^^concerns, ^^or ^^suggestions!")

    return ''.join(bot_comment)

def threader(comment):
    comment.reply(generate_counts(comment.submission.id))
    return

key_phrase = '!aita\_bot'


if __name__ == '__main__':
    while True:
        for comment in subreddit.stream.comments(skip_existing=True):
            if key_phrase in comment.body:
                t = threading.Thread(target=threader, args=(comment, ))
                t.daemon = False
                t.start()

