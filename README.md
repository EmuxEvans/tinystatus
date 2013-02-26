# TinyStatus - A P2P short-status network you can fit in your email sig.
by Cathal Garvey
@onetruecathal (on Twitter/TinyStatus, but the latter has no auth! ;))
cathalgarvey@cathalgarvey.me
https://gitorious.org/~cathalgarvey
http://www.indiebiotech.com

## What is TinyStatus?
TinyStatus is a peer to peer microstatus server/client script written in pure python, in as few 80-character lines as I could manage.

TinyStatus is heavily inspired by E.W. Felten's TinyP2P, code for which is included as per its CC-BY-NC-SA license for reference.

Like TinyP2P, TinyStatus establishes a (small, poorly scaleable) network of servers hosting content that clients can poll and fetch from. Unlike TinyP2P, the content in this case is clients' short status messages, which consist of a username, up to 150 characters of text, and a timestamp and cryptographic proof-of-work to deter spamming.

Unlike TinyP2P, TinyStatus is not only a fetching network, but a posting network; users can connect to arbitrary servers and post their statuses, which will be distributed among other servers as transactions occur between the servers in the course of normal activity.

Unfortunately, TinyStatus is also a lot larger than TinyP2P; I attribute this to the fact that TinyP2P can take advantage of OS-level functions for management of locally served files, whereas TinyStatus requires code to manage a message database in-memory. While I could save statuses to small text files to achieve a result like TinyP2P, I think it's better to get efficiency and function than scrounge a few lines of code at the cost of constant hard drive read/write cycles. In addition, if HDD read/writes were common with TinyStatus, then I'd have a hard time running a personal server on a Raspberry Pi without wearing out the SD card! ;)

## Why did you write this?
TinyP2P was written in response to government proposals in the US to illegalise file-sharing protocols. The aim of the script was to demonstrate that, with P2P filesharing reduced down to 15 lines of code which will fit nicely in an email signature, there was little hope that any level of regulation would work. Big servers might die, but a thousand TinyP2Ps or their equivalents would bloom.

In Ireland, there is a rather disgusting political campaign in progress to try and regulate Free Speech (which is already lacking in Ireland) on social networks. The rhetoric is that social networks like Twitter and (ugh) Facebook allow this new phenomenon of anonymous bullying called "cyberbullying" which was somehow not a problem in the prior decade's worth of internet use, nor in the decade before that of ubiquitous txt messaging, nor for centuries before that with the postal system.

To push this agenda, Irish politicians have taken to blaming every suicide in the country on cyberbullying, transforming the loss of a person into a political tool.

They are also attempting to paint social networking as a threat to social stability: in a press release asking for commentary on "What to do" (not "Should?", but "What?") about social networking, a government working group described "Unfettered Commentary" as if it were a problem requiring a solution.

The reason for this is pretty simple: Twitter and (ugh) Facebook allow Irish citizens to share the burden of oversight upon their government. Word-of-mouth has become so swift and absolute in Ireland, that every revelation of corruption and false democracy in Ireland is coming to light instantly. Our wealthy, austerity-pushing government don't like being told that their policies don't work, never have worked, and never will work. They don't like to be called out in public, in front of other citizens. They don't like mediums where we can talk back: they want us to live in a world where they can silence our questions, and provide only the answers they want to give in a one-way manner. They want their podium back.

I plan to make a submission to their panel, consisting of this script and some brief notes on why regulation of free speech will not only be an injust and embarrassing imposition on the citizenry of Ireland, but that it will do nothing to stop us from criticising their terrible policies in public, on social networks that we will build if necessary to prevent their censorship.

Besides, P2P is awesome. I have been meaning for some time to bulid a P2P twitter, although I actually want to make a real, workable, DHT-based status network incorporating pubkey authentication of users. If or when I get the time to do that in between biohacking and parenting, I'll probably make use of some of the object code in TinyP2P!

## That code is HIDEOUS
Well, yes. That's what happens when you take a language designed to enforce clarity and evenly spaced code, and cram it into as few lines and statements as possible!

Some of the ugliness comes from lessons learned from TinyP2P, which made liberal use of tricky list unpacking to achieve the same result as for or while loops, and use of the "and" and "or" operators to conditionally run code based on the results of a quick test, or to alter the return value of a lambda function.

However, some of the ugliness is new: TinyP2P didn't use objects, but I decided that the value of being able to operate in-place on object attributes was worth the trouble, and I faced new challenges to code readability.

In particular, some quirks of Python's interpreter forced some nasty compromises. For example, Python doesn't like to see more than one set of colons per line, so I couldn't do:
```python
class myClass(): def __init__(s, foo): s.foo = foo```

However this was ok:
```python
class M:N,r=lambda s,x:SA(s,'v',x),lambda s,x=0:[s.t,s.n,s.m[:150],x or s.v]'''

..but at the cost of another quirk, wherein if a statement is provided on the same line as "class foo():", then parsing of class attributes (including methods) does not continue to the next line.

Because it was unacceptable to sacrifice a whole line just for "class foo():", I opted to forego python's beautifying indentation format, and instead to explicitly set class attributes:
```python
M.P=lambda s:[s.N(x+1) for x in takewhile(lambda x:s.H(x)>POW,count())].pop()
```
However, some of the tricks I discovered actually improved readability, I think. For example, the import block at the top uses an exec-based hack (yes, exec. There is no legitimate use for this awful function unless you're minimising code.) to compress a multiline, convoluted shortcutting block for class/function imports into a single string expansion. Adding a new import is as simple as adding a colon to the end of the string, followed by the module name and the items you want imported from it.

For compressing code down to an absolute minimum, you can do something similar to the entire script, flattening it into a single line string with line breaks delimited by semicolons, and exec'ing the split lines. When the script is ready, I plan to build this in with a quick replace() method on the script to make it function as normal even if lines are broken and interrupted with "> " character pairs by nested email quoting, so that the script "self repairs" from email reply/forward blocks (provided the leading and trailing bits of the script are manually fixed, of course..). :)

## Spam?
Oh yea! TinyP2P had a hmaccing system for using a password to authenticate to small networks, which was really clever (but probably vulnerable to replay attacks, and didn't encrypt traffic at all).

I decided to hack that out, because a password isn't much use to a microstatus network in my opinion. However, because TinyStatus allows posting to remote servers of new data, it has a problem TinyP2P didn't: Spammers!

To counter spammers, TinyStatus servers will reject any message that doesn't have a suitable proof-of-work token. This is a small numeric value attached to the time, name and message values of the message, which modifies the hash value of the message so that it appears "pleasing" to the server; literally, that it has at least three leading zero characters. Because of the magic of cryptographic hash functions, there is no practical way to generate a proof-of-work token except iterating over thousands of potential numbers until one of them works. With three leading zeroes, generating a useful token requires a few seconds, varying randomly between messages.

This means that someone wanting to send a hundred new messages will need to spend about five hundred seconds generating useful tokens. It's doable, but it's more far costly to the spammer than it would be without tokens!

## Platforms?
TinyStatus is written in pure Python 3, so it should run on all major platforms provided they have Python 3 installed. If you count iPhones as "platforms" and not simply "Tiny Steve Jobs", then you're out of luck, because that "Platform" doesn't allow anything not personally vetted by the real owners of the phones: Apple. Android, on the other hand, can be loaded with Python 3 through the Android Scripting Layer, although because I'm too lazy to investigate options for a graphical interface or any other such niceities, you'll have to make do with the terminal interface.

Personally, I want to get this on my Kindle Touch, but I can't get it to successfully build Python 3, and cross-compiling Python is one of those jobs that only masochists bother attempting. I've tried installing through optware; no luck, sadly.

## Improvements?
A lot of improvements can be made with third-party modules, but TinyStatus must be standalone, so only native library code or ubiquitous addons should be considered.

TinyStatus uses Python's built-in XMLRPC system for servers and clients. It's a beautifully simple system for establishing a networking protocol, but XML itself has huge overheads for data like TinyStatus; the XML formatting is likely to be many times the size of most requests. JSON-RPC would be a much more suitable format, but Python doesn't have a builtin JSON-RPC library.

If one were to include PyCrypto in the list of requirements, a 10-20 extra lines of code could implement pubkey authentication so that users couldn't simply falsify their names and post as other users. This would require that servers remember which pubkey they first saw used by which usernames, and thereafter only honour messages signed by the same pubkey. The main problems are the availability of PyCrypto, which is not included in Python by default, and compilation of PyCrypto for smaller platforms that cannot compile their own code easily, like Android (I'm stunned that there's so little effort put into putting "make" on Android).

Additionally, if PyCrypto was being used anyway, one could encrypt the network traffic, which would provide a small measure of protection against network analysis to determine who is the author of what messages, and who follows who.

Fundamentally though, TinyStatus is a limited architecture; without a more advanced method of organising the network, scaling TinyP2P beyond a few tens of servers is likely to lead to massive congestion of server traffic and very slow clients.

The path to enlightenment here is to implement a DHT architecture where users can register pubkeys in a DHT for their username, publish messages to the DHT at a defined location or based on the hash of each individual message, and have a list for their followers of hashes to fetch for each message. That way, servers need only store the data that hashes close to the servers' own pubkey hash, and can fetch pubkeys to verify message authenticity from the DHT as required. Additionally, as the DHT hash locations for usernames and pubkeys would be unique, servers could easily agree on which users correspond to which pubkeys, making users more unique and trustworthy without requiring a password-based or central certification platform like Twitter or Facebook. This is ultimately something I'd love to try, but as there are no pure python 3 DHT implementations out there that I can see so far, I'll either have to write my own or await the Twisted project's slow, grudging migration to modern Python.
