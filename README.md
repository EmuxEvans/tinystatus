# TinyStatus - A P2P short-status network you can fit in your email signature.
Copyright 2013 Cathal Garvey, License: GNU Affero General Public License v3

* @onetruecathal (on Twitter/TinyStatus, but the latter has no auth! ;) )
* cathalgarvey@cathalgarvey.me
* https://www.gittip.com/onetruecathal/ Gittip me?
* https://gitorious.org/~cathalgarvey
* http://www.indiebiotech.com

## Dedication
Pat Rabbitte: You won't prevent us from speaking, only yourself from hearing.

## What is TinyStatus?
TinyStatus is a peer to peer microstatus server/client script written in pure
python, in as few 80-character lines as I could manage.

TinyStatus is heavily inspired by E.W. Felten's TinyP2P, code for which is
included (as per its CC-BY-NC-SA license) for reference.

Like TinyP2P, TinyStatus establishes a (small, poorly scaleable) network of
servers hosting content that clients can poll and fetch from. Unlike TinyP2P,
the content in this case is clients' short status messages, which consist of a
username, up to 150 characters of text, and a timestamp and cryptographic
proof-of-work to deter spamming.

Unlike TinyP2P, TinyStatus is not only a fetching network, but a posting
network; users can connect to arbitrary servers and post their statuses, which
will be distributed among other servers as transactions occur between the
servers in the course of normal activity.

Unfortunately, TinyStatus is also a lot larger than TinyP2P; I attribute this to:
* TinyP2P can take advantage of OS-level functions for management of
  locally served files.
* TinyP2P doesn't contain multiline try:catch statements to prevent crashes due
  to bad server data (which would make attacking the network trivial).
* TinyStatus includes anti-flood/anti-spam features not required in TinyP2P.

## How do I use TinyStatus?
There are several modes of use in TinyStatus. One is for hosting a node/server,
three are for posting/fetching from servers, and two are to directly add/remove
"follows" from the local database.

* Serve:  _python3 TinyStatus.py serve (hostname) (portnumber) (otherservers)_
* Post:   _python3 TinyStatus.py post (server) (username)_
* Update: _python3 TinyStatus.py update (server)_
* Find:   _python3 TinyStatus.py find (server) (findstring(s))_
* Follow: _python3 TinyStatus.py addfollow (follow(s))_
* Remove: _python3 TinyStatus.py remove (follow(s))_

You can follow any search string (technically a regex string, for the geeks),
whether a username, hashtag, time, date, whatever. To see anything written by a
user or said *about* that user, follow "@user". To see *only* stuff posted by that
user, use "^@user".

To search, use the find command with one or more search strings, which have the
same format as "follow". To update follows, just specify the server.

To post, specify the target host server and your desired username. There is *no*
account control in this network, so anyone can impersonate anyone else. Sorry!
You will be presented with a prompt for your message, which can be up to 150
characters long.

Servers always host on localhost, but the terminal command "hostname" is what is
sent to remote servers as the hostname by which to look the local server up. So,
when starting a server, use a hostname and port number that is publicly visible.
The only rule is: Don't host a node *and* use posting/fetching in the same
folder, or database conflicts may occur. If you want to host a node, copy the
script into a new folder first, optionally with your database file "D" that may
contain a list of known peers.

## Why did you write this?
TinyP2P was written in response to government proposals in the US to illegalise
file-sharing protocols. The aim of the script was to demonstrate that, with P2P
filesharing reduced down to 15 lines of code which will fit nicely in an email
signature, there was little hope that any level of regulation would work. Big
servers might die, but a thousand TinyP2Ps or their equivalents would bloom.

When TinyStatus was written, there was a nasty political campaign to attack free
speech online under the guise of (as usual) "protecting children". Among the
tactics employed was a hyping-up of "cyberbullying" (still ongoing) and a
"pity me" campaign of politicians saying how hurt they felt when people criticised
their pro-austerity policies on Twitter. In a press release asking for commentary 
on "What to do" (not "Should?", but "What?") about social networking, a government
working group described "Unfettered Commentary" as if it were a problem requiring
a solution.

Like TinyP2P, I wrote TinyStatus so that it would be small enough to disseminate
trivially in fora, emails and even printed on paper. It was my "submission"
to the public consultation on Free Speech on Social Media (not the actual name
of the consultation, much as it should have been).

Nobody took any notice of TinyStatus, of course, but it was a fun project, and
for me it was part of my maturation to realising the intense political nature
of our ability to program our own computers. Programming allows us to write our way
out of some forms of oppression. It should be seen as a key democratic skill in
the modern era.

## That code is HIDEOUS
You think it's bad now? Look back through the commits to when I was trying to
horseshoe in some object oriented programming. Making classes in as few lines as
possible leads to the ugliest possible code.

But yes, in the interest of fitting as much useful code into 80 characters as is
humanly possible, I compromised a great deal on code readability. Sorry!

## Spam?
Oh yea! TinyP2P had a hmaccing system for using a password to authenticate to
small networks, which was really clever (but probably vulnerable to replay
attacks, and didn't encrypt traffic at all).

I decided to hack that out, because a password isn't much use to a microstatus
network in my opinion. However, because TinyStatus allows posting to remote
servers of new data, it has a problem TinyP2P didn't: Spammers!

To counter spammers, TinyStatus servers will reject any message that doesn't
have a suitable proof-of-work token. This is a small numeric value attached to
the time, name and message values of the message, which modifies the hash value
of the message so that it appears "pleasing" to the server; literally, that it
has at least three leading zero characters. Because of the magic of
cryptographic hash functions, there is no practical way to generate a
proof-of-work token except iterating over thousands of potential numbers until
one of them works. With three leading zeroes, generating a useful token requires
a few seconds, varying randomly between messages.

This means that someone wanting to send a hundred new messages will need to
spend about five hundred seconds generating useful tokens. It's doable, but it's
more far costly to the spammer than it would be without tokens!

## Platforms?
TinyStatus is written in pure Python 3, so it should run on all major platforms
provided they have Python 3 installed. It only uses modules and functions
distributed as part of the Python 3 core.

## Improvements?
For the purposes of this section, let's pretend code brevity is no longer a concern.

A lot of improvements can be made with third-party modules, but "politically",
TinyStatus must be standalone, so only native library code or ubiquitous addons
should be considered.

Still, here are some immediate and obvious improvements:

* Use of SQLite3 for databasing instead of the flat file.
* Storing known servers, scoring of servers by reliability.
* Adding a TOFU (trust-on-first-use) public-key system for authentication.
* Use of a simple federation protocol or DHT for servers to minimise traffic.
* Expiry of old data.
* Rewrite in RPython.

If we ignore avoiding third-party code or code that won't compile easily on embedded:

* PyNaCl for authentication and encryption of private messages.
* JSON-RPC instead of XMLRPC, or Flask mini-webapps hosted through Pagekite/similar
* Wordpress server plugin? :)
