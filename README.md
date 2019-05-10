# aita_bot

A Reddit bot for the [AmITheAsshole](https://www.reddit.com/r/AmItheAsshole/) subreddit written using praw and the Python threading library.

The bot constantly runs a loop reading in new comments from the subreddit.  When one is found that contains the phrase 
'!aita_bot' the bot will reply with counts and %'s of the votes in that thread. (YTA, NTA, ESH, NAH, or INFO).

## The technical stuff.

The main loop of the bot runs in the main thread.  It reads in every new comment and looks for the '!aita_bot' phrase.
When the phrase is found, the comment is put in a Queue to be picked up in its own thread.  Several threads are constantly checking 
for new comments in the queue.  When a thread picks up a comment it runs a function that will take the submission_id from the comment (the
reddit submission that contains the comment), grab *every* comment from that submission, and use a regular expression to try to match one of the 
votes in question.  When a vote is found, it is incremented as a key in a defaultdict.  Once every comment has been crawled, a reply is
constructed using the defaultdict keeping track of the votes.  That reply message is then sent as a comment back to reddit, right underneath
the comment that called the bot, and the thread goes back to looking for comments in the Queue.

I've chosen to run the the vote gathering and replying methods within their own thread because the operations can be very time consuming
due to the large number of reddit API calls that have to be made. I wanted to keep the main thread running as often as possible to pick up 
new comments.  I considered multiprocessing, but the operatons don't seem to put a large strain on the CPU.

The bot runs on a [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) running Raspbian.  
As of now (5/9/2019) I'm still making enough significant changes to the bot that I probably won't leave it running very often.
I expect that to change within the next week or so, as I iron out error handling and the like. 

### Example comment from the bot:

YTA has 11% of all of the comments with votes in this submisson. (102/901 total comments)

NAH has 16% of all of the comments with votes in this submisson. (152/901 total comments)

NTA has 67% of all of the comments with votes in this submisson. (612/901 total comments)

ESH has 3% of all of the comments with votes in this submisson. (31/901 total comments)

INFO has 0% of all of the comments with votes in this submisson. (4/901 total comments)

<sup>I am the AITA bot! Post '!aita_bot' in any AmITheAsshole submission and I'll reply to your comment with counts and percentages of how users voted in this thread.</sup>

<sup>Feel free to message the creator, /u/blarmon_kek with any questions, concerns, or suggestions!</sup>
