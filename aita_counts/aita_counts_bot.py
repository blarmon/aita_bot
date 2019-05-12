import re
import time
from collections import defaultdict
import threading
from queue import Queue

import config
import logger
import write_out_data

reddit = config.reddit_config
subreddit = reddit.subreddit('AmITheAsshole')

# TODO.  grab the most upvoted comment for each type of vote and link to it.  that's good stuff.
# TODO clean up variable shadowing
# TODO error handling

# TODO ERROR HANDLING ON THE REPLY

# todo!!!  i need to put a lock on my data and logging files!!!!  data will get jumbly otherwise

def generate_counts(comment):
    submission = reddit.submission(id=comment.submission.id)
    aita_dict = defaultdict(int)

    try:
        submission.comments.replace_more(limit=None)
    except AssertionError as e:
        logger.log_error(e)
        time_to_reset = reddit.auth.limits['reset_timestamp'] - time.time()
        time.sleep(time_to_reset)
        q.put(comment)
        return

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
            reply = generate_counts(comment)

            if reply:
                # TODO TRY EXCEPT HERE!  COULD ALWAYS ENCOUNTER RATE LIMITING ISSUES
                comment.reply(reply)
                write_out_data.write_new_comment(time.time(), reply)

            q.task_done()


if __name__ == '__main__':

    key_phrase = '!aita\_bot'
    q = Queue()
    aita_regex = re.compile(r'(YTA|NTA|ESH|NAH|INFO)')

    for _ in range(5):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    while True:
        for comment in subreddit.stream.comments(skip_existing=True):
            print(reddit.auth.limits)
            if key_phrase in comment.body:
                print('here')
                q.put(comment)

