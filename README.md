# You Forgot To Share Your Google Doc!

A simple reddit bot to tell people that their Google Docs links are not publicly
accessible.

## Functionality

YFTSYGD crawls reddit threads, looking for Google Docs links in the top-level
comments. If it finds one that it can't access, it will leave the following
comment:

> Hello! It looks like you forgot to share your Google Doc. You'll need to get a shareable link so the rest of us can see it. To do that, click the blue 'Share' button in the top right corner of the document, then click 'Get Shareable Link.' It is recommended that you also enable others to comment; this will allow them to leave line edits.
>
> -----
>
> I am a bot, bleep bloop. This comment was posted automatically. [Source code.](https://github.com/flyingpimonster/yftsygd) My human overlord is /u/flyingpimonster

If it comes across a link that it has commented on already, but has been fixed,
it will strike out its original comment and place a notice at the top:

> Edit: It looks like it's working now.

## Usage

The following tutorial describes how to set up the bot. It assumes you know the
basics of creating scheduled tasks, running scripts, etc. If it sounds like too
much work, you can PM me (/u/flyingpimonster) and ask me to run it for your sub
(assuming you're a moderator). Note that I can in no way guarantee the continued
availability of the service.

To run the bot, create a file called `praw.ini` using the following template:

    [YFTSYGD]
    client_id=<client-id>
    client_secret=<client-secret>
    user_agent=python:net.flyingpimonster.redditbots.yftsygd:v0.0.1 (by /u/flyingpimonster)
    username=<username>
    password=<password>

Make sure you fill in all the fields. You will need to
[create a script application](https://www.reddit.com/prefs/apps/) in your reddit
preferences to get a client ID and secret.

Next, install `praw` ([Python Reddit API Wrapper](https://github.com/praw-dev/praw))
using pip: `pip3 install praw --user`

Then, run `python3 main.py`. It should print its username and the date/time if
successful.

YFTSYGD must be told where to look for Google Docs links. This is done through
command line arguments. To crawl a certain thread, put its thread ID in the
command line arguments, like this: `python3 main.py 7uuvat` (that is a test
post that you can use if you want to make sure it works.)

To crawl a subreddit's sticky threads, use the name of the subreddit as an
argument, like this: `python3 main.py r/examplesubreddit`. This will look for
sticky threads in r/examplesubreddit and crawl the first thread that includes
the word "critique" in its title. This behavior currently cannot be changed
except by modifying the code.
