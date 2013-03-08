# TinyStatus - A P2P short-status network you can fit in your email signature.
Copyright 2013 Cathal Garvey, License: GNU Affero General Public License v3

* @onetruecathal (on Twitter/TinyStatus, but the latter has no auth! ;) )
* cathalgarvey@cathalgarvey.me
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

Unfortunately, TinyStatus is also a lot larger than TinyP2P; I attribute this to
the fact that TinyP2P can take advantage of OS-level functions for management of
locally served files, and TinyP2P doesn't contain multiline try:catch statements
to prevent crashes due to bad server data (which would make attacking the
network trivial).

## How do I use TinyStatus?
There are several modes of use in TinyStatus. One is for hosting a node/server,
three are for posting/fetching from servers, and two are to directly add/remove
"follows" from the local database.

* Serve:  _python3 TinyStatus.py serve (hostname) (portnumber) (otherservers)_
* Post:   _python3 TinyStatus.py post (server) (username)_
* Update: _python3 update (server)_
* Find:   _python3 find (server) (findstring(s))_
* Follow: _python3 addfollow (follow(s))_
* Remove: _python3 remove (follow(s))_

I will intermittantly be hosting a TinyStatus server at https://tinystatus.pagekite.me
which you can use to get started and try it out. Consider following "^@onetruecathal"
to get updates from me or anyone pretending to be me.

You can follow any search string (technically a regex string, for the geeks),
whether a username, hashtag, time, date, whatever. To see anything written by a
user or said *about* that user, follow "@user". To see *only* stuff posted by that
user, use "^@user".

To post, specify the target host server and your desired username. There is *no*
account control in this network, so anyone can impersonate anyone else. Sorry!
You will be presented with a prompt for your message, which can be up to 150
characters long.

To search, use the find command with one or more search strings, which have the
same format as "follow". To update follows, just specify the server.

Servers always host on localhost, but the terminal command "hostname" is what is
sent to remote servers as the hostname by which to look the local server up. So,
when starting a server, use a hostname and port number that is publicly visible.
If you don't have a publicly visible hostname (most likely), read on:

Included is the excellent "pagekite.py" script. To run this, you'll *also*
need python 2 installed, because it doesn't work with modern Python, sadly. But,
once you have python 2, you can use it to launch pagekite.py like this:
* python2 pagekite.py (portnumber) (desiredsubdomain).pagekite.me

..and the pagekite.py script will guide you through signing up for a free month
of use and see if you can register desiredsubdomain.pagekite.me as your server
name.

Then start your server like so:
* python3 TinyStatus.py serve https://(desiredsubdomain).pagekite.me (portnumber) (otherserver(s))

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

In Ireland, there is a rather disgusting political campaign in progress to try
and regulate Free Speech (which is already lacking in Ireland) on social
networks. The rhetoric is that social networks like Twitter and (ugh) Facebook
allow this new phenomenon of anonymous bullying called "cyberbullying" which was
somehow not a problem in the prior decade's worth of internet use, nor in the
decade before that of ubiquitous SMS messaging, nor for centuries before that
with the postal system.

To push this agenda, Irish politicians have taken to blaming every suicide in
the country on cyberbullying, transforming the loss of a person into a political
tool. They are also attempting to paint social networking as a threat to social
stability: in a press release asking for commentary on "What to do" (not
"Should?", but "What?") about social networking, a government working group
described "Unfettered Commentary" as if it were a problem requiring a solution.

The reason for this is pretty simple: Twitter and (ugh) Facebook allow Irish
citizens to share the burden of oversight upon their government. Word-of-mouth
has become so swift and absolute in Ireland, that every revelation of corruption
and false democracy in Ireland is coming to light instantly. Our wealthy,
austerity-pushing government don't like being told that their policies don't
work, never have worked, and never will work. They don't like to be called out
in public, in front of other citizens. They don't like mediums where we can talk
back: they want us to live in a world where they can silence our questions, and
provide only the answers they want to give in a one-way manner. They want their
podium back.

I plan to make a submission to their panel, consisting of this script and some
brief notes on why regulation of free speech will not only be an injust and
embarrassing imposition on the citizenry of Ireland, but that it will do nothing
to stop us from criticising their terrible policies in public, on social
networks that we will build if necessary to prevent their censorship.

Besides, P2P is awesome. I have been meaning for some time to bulid a P2P
twitter, although I actually want to make a real, workable, DHT-based status
network incorporating pubkey authentication of users.

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
provided they have Python 3 installed.

If you count iPhones as "platforms" and not simply "Tiny Steve Jobs", then
you're out of luck, because that "Platform" doesn't allow anything not
personally vetted by the real owners of the phones: Apple.

Android, on the other hand, can be loaded with Python 3 through the Android
Scripting Layer, although because I'm too lazy to investigate options for a
graphical interface or any other such niceities, you'll have to make do with the
terminal interface.

## Improvements?
A lot of improvements can be made with third-party modules, but TinyStatus must
be standalone, so only native library code or ubiquitous addons should be
considered.

TinyStatus uses Python's built-in XMLRPC system for servers and clients. It's a
beautifully simple system for establishing a networking protocol, but XML itself
has huge overheads for data like TinyStatus; the XML formatting is likely to be
many times the size of most requests. JSON-RPC would be a much more suitable
format, but Python doesn't have a builtin JSON-RPC library.

If one were to include PyCrypto in the list of requirements, a 10-20 extra lines
of code could implement pubkey authentication so that users couldn't simply
falsify their names and post as other users. This would require that servers
remember which pubkey they first saw used by which usernames, and thereafter
only honour messages signed by the same pubkey. The main problems are the
availability of PyCrypto, which is not included in Python by default, and
compilation of PyCrypto for smaller platforms that cannot compile their own code
easily, like Android (I'm stunned that there's so little effort put into putting
"make" on Android).

Additionally, if PyCrypto was being used anyway, one could encrypt the network
traffic, which would provide a small measure of protection against network
analysis to determine who is the author of what messages, and who follows who.

Fundamentally though, TinyStatus is a limited architecture; without a more
advanced method of organising the network, scaling TinyStatus beyond a few tens
of servers is likely to lead to massive congestion of server traffic and very
slow clients. Making a twitter-killer was never the point; it can be done, but
unless our glorious leaders decide to attack free speech on Twitter, there is
little incentive to do so right now.
