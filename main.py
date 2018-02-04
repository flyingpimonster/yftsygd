#!/usr/bin/python3
import praw
import re
import os
import urllib
import sys
import datetime

body = "Hello! It looks like you forgot to share your Google Doc. To do that, click the blue 'Share' button in the top right corner of the document, then click 'Get Shareable Link.' The link you posted should then work. It is recommended that you also change 'anyone with the link *can view*' to 'anyone with the link *can comment.*' This way, people can leave line edits."
footer = "\n\n-----\n\n^(I am a bot, bleep bloop. This comment was posted automatically.) [^Source ^code.](https://github.com/flyingpimonster/yftsygd) ^(My human overlord is /u/flyingpimonster)"

message = body + footer
editmessage = "Edit: It looks like it's working now.\n\n~~" + body + "~~" + footer

# Create the Reddit instance
reddit = praw.Reddit("YFTSYGD")

newverified = []

def updateComment(comment):
    try:
        comment.edit(editmessage)
        print("      Reply: " + comment.id + " (updated)")
    except praw.exceptions.APIException as err:
        print("      ERROR:", err)


def replyToCommment(comment):
    try:
        reply = comment.reply(message)
        print("      Reply: " + reply.id + " (new)")
    except praw.exceptions.APIException as err:
        print("      ERROR:", err)

def processComment(comment):
    if comment.id in verified:
        return

    doclinks = re.findall("https?:\/\/(?:docs|drive).google.com\/[A-Za-z0-9_/?=\-]*", comment.body)

    ourComment = None
    for reply in comment.replies:
        if reply.author == reddit.user.me().name:
            ourComment = reply
            break

    for link in doclinks:
        try:
            with urllib.request.urlopen(link) as req:
                # check if we've been redirected to a login page, which means we
                # don't have access
                if re.search("ServiceLogin", req.geturl()):
                    if ourComment is None:
                        # post a comment
                        print("    Comment: " + comment.id)
                        replyToCommment(comment)
                        break

                else:
                    # add this comment to the list of comments not to check
                    # again
                    newverified.append(comment.id)

                    if ourComment is not None:
                        # we already replied, make sure the comment is updated
                        # because the link works now
                        if not re.search("Edit", ourComment.body):
                            print("    Comment: " + comment.id)
                            updateComment(ourComment)
                            break
                    else:
                        print("    Comment: " + comment.id + " (ok)")

        except urllib.error.HTTPError as err:
            print("    Comment: " + comment.id)
            print("      ERROR:", err)

def processThread(thread):
    print("  Thread: " + thread.id + " " + thread.title)

    for comment in thread.comments:
        processComment(comment)

def processSubreddit(subName):
    # look for sticky threads, process ones that have "critique" in the title

    print("Subreddit: /r/" + subName)

    subreddit = reddit.subreddit(subName)

    stickyIndex = 1
    lastSticky = ""
    while True:
        sticky = subreddit.sticky(stickyIndex)
        if(sticky.id == lastSticky):
            break
        else:
            lastSticky = sticky.id

        if re.search("critique", sticky.title, re.IGNORECASE):
            processThread(sticky)
            break

        stickyIndex += 1

now = datetime.datetime.now()

# debug info
print("Running as /u/" + reddit.user.me().name + " on " + now.strftime("%Y-%m-%d %H:%M:%S"))

# clear verified.txt once a week, on Sunday (which is day 6 in python)
if (now.weekday() == 6 and now.hour == 0 and now.minute < 10):
    print("Clearing verified.txt")
    with open("verified.txt", "w"):
        pass

# Load list of already verified comments
try:
    with open("verified.txt", "r") as file:
        verified = file.read().splitlines()
except:
    verified = []

# read the command line arguments
for arg in sys.argv[1:]:
    if arg.startswith("r/"):
        # process a sub's critique stickies
        processSubreddit(arg[2:])
    else:
        # process a particular thread
        processThread(reddit.submission(arg))

# Write newly verified comments to verified.txt
with open("verified.txt", "a") as file:
    for item in newverified:
        file.write("%s\n" % item)

# Print a trailing newline to the output, for readability
print("")
