# Original TinyP2P Post:
## TinyP2P
*The World's Smallest P2P Application*
*Written by Ed Felten, with help from Alex Halderman.*

TinyP2P is a functional peer-to-peer file sharing application, written in fifteen lines of code, in the Python programming language. I wrote TinyP2P to illustrate the difficulty of regulating peer-to-peer applications. Peer-to-peer apps can be very simple, and any moderately skilled programmer can write one, so attempts to ban their creation would be fruitless.

(Each line has 80 characters or fewer. The first line doesn't count -- it's a label for human readers and is ignored by the computer.)

My goal in creating this program is not to facilitate copyright infringement. I do not condone copyright infringement. Nothing about the program's design is optimized for the sharing of infringing files. The program is useful mainly as a proof of concept. A more practical program would be faster, more secure, and more resilient against failure. But that would require a few more lines of code!

The TinyP2P code is available for download at http://www.freedom-to-tinker.com/tinyp2p.py.

##How It Works
The program creates a small-world network, which might be used by a group of friends or business associates to share files. The program does not work well for very large networks; instead, many small networks can coexist. Each network is protected by a password; a network can be accessed only by people who know its password. (But networks are not secure against attackers who can eavesdrop on their traffic.)

The program uses standard communication protocols: HTTP and XML-RPC. HTTP is the same protocol used by web browsers to fetch pages, and XML-RPC is widely used to provide web services.

The program can be run in one of two modes, server or client. When run as a server, the program connects to a network of other servers, and makes all of the files in the current directory available for downloading by users of the network. (Files deposited into that directory while the server is running will become available immediately to other users.) To run the program as a server, you type this command:

    python tinyp2p.py password server hostname portnum [otherurl]*

Here password is the password for the network, hostname and portnum will be used to construct the URL on which the server will listen (http://hostname:portnum), and otherurl (which is optional) is the URL of another server that is already running as part of the network. (Otherurl will be used to hook up your server to the network. If you don't provide an otherurl, the program will assume that your server is starting a new network.)

To run the program as a client, you type this command:

    python tinyp2p.py password client serverurl pattern

Here password is the network's password, serverurl is the URL of a server that belongs to the network, and pattern is a character string. This command looks at every file being shared by every server on the network. A file is downloaded, and stored in the current directory, if two things are true: (a) the file's name contains the substring pattern, and (b) there is not already a file of the same name in the current directory. (Note for ubergeeks: pattern can actually be a Python regular expression, which is matched against filenames using Python's re.search library call.)

Note that if you run a client in the same directory where you're running a server, then files downloaded by the client will automatically be redistributed by the server. Depending on your circumstances, this may or may not be what you want. Also note that you can run multiple servers, belonging to different networks, in the same directory.

This work is licensed under a [Creative Commons License][http://web.archive.org/web/20070927205613/http://creativecommons.org/licenses/by-nc-sa/2.0/].
