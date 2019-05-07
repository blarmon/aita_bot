import re
from collections import defaultdict
import config

reddit = config.reddit_config

subreddit = reddit.subreddit('AmItheAsshole')


def generate_counts(submission_id):
    submission = reddit.submission(id=submission_id)

    aita_regex = re.compile(r'(YTA|NTA|ESH|NAH|INFO)')
    sb = []

    # top level comments
    # aita_dict_top = defaultdict(int)
    #
    # for top_level_comment in submission.comments:
    #     matcher = None
    #     if hasattr(top_level_comment, 'body'):
    #         matcher = aita_regex.search(top_level_comment.body)
    #     if matcher:
    #         aita_dict_top[matcher.group(1)] += 1
    #
    # total_votes_top = sum([v for v in aita_dict_top.values()])
    #
    # for k, v in aita_dict_top.items():
    #     sb.append(f"{k} has {str((v/total_votes_top)*100).split('.')[0]}% of the top level comments with votes. ({v}/{total_votes_top})" + "\n\n")
    # sb.append('\n\n&nbsp;')


    # all comments
    aita_dict_all = defaultdict(int)

    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        matcher = aita_regex.search(comment.body)
        if matcher:
            aita_dict_all[matcher.group(1)] += 1

    total_votes_all = sum([v for v in aita_dict_all.values()])

    for k, v in aita_dict_all.items():
        sb.append(f"{k} has {str((v/total_votes_all)*100).split('.')[0]}% of all of the comments with votes in"
                  f" this submisson. ({v}/{total_votes_all} total comments)" + "\n\n")

    sb.append(
        "\n\n^I ^am ^the ^AITA ^bot!  ^Post ^'!aita_bot' ^in ^any ^AmITheAsshole ^submission ^and ^I'll ^reply ^to ^your ^comment ^with ^counts ^and ^percentages"
        " ^of ^how ^users ^voted ^in ^this ^thread.")
    sb.append('\n\n')
    sb.append("^^Feel ^^free ^^to ^^message ^^the ^^creator, ^^/u/blarmon_kek ^^with ^^any ^^questions ^^or ^^concerns!")

    return ''.join(sb)



key_phrase = '!aita\_bot'

while True:
    for comment in subreddit.stream.comments(skip_existing=True):
        print(comment.body)
        if key_phrase in comment.body:
            comment.reply(generate_counts(comment.submission.id))

