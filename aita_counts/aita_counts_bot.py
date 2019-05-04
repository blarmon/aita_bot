import praw
import re
from collections import defaultdict

USERNAME = 'aita_bot'
PASSWORD = 'J2ET2DDfnDGnJmrd'
USERAGENT = "This bot created by /u/blarmon_kek"

reddit = praw.Reddit(client_id='9_-k277E1j_HIA',
                    client_secret = '1u2vbf2sefNW4cI9B2X0aHMtgPE',
                    user_agent=USERAGENT,
                    username=USERNAME,
                    password=PASSWORD,)

subreddit = reddit.subreddit('AmItheAsshole')


def generate_counts(submission_id):
    submission = reddit.submission(id=submission_id)

    aita_regex = re.compile(r'(YTA|NTA|ESH|NAH|INFO)')
    aita_dict = defaultdict(int)

    for top_level_comment in submission.comments:
        matcher = None
        if hasattr(top_level_comment, 'body'):
            matcher = aita_regex.search(top_level_comment.body)
        if matcher:
            aita_dict[matcher.group(1)] += 1

    total_votes = sum([v for v in aita_dict.values()])
    sb = []

    for k, v in aita_dict.items():
        sb.append(f"{k} has {str((v/total_votes)*100).split('.')[0]}% of the top level comments. ({v}/{total_votes})" + "\n\n")

    sb.append(
        "I am the AITA bot!  Post '!aita_bot' in any AmITheAsshole submission and I'll reply to your comment with counts and percentages"
        " of how people voted in this thread.  Currently the bot only looks at top level comments on any submission.")

    return ''.join(sb)



key_phrase = '!aita\_bot'

while True:
    for comment in subreddit.stream.comments(skip_existing=True):
        if key_phrase in comment.body:
            comment.reply(generate_counts(comment.submission.id))

