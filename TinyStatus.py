#!/usr/bin/env python3
for x in ('itertools takewhile count:os.path exists:hashlib sha256:time time ct'
'ime:json dump dumps load loads:sys argv exit:xmlrpc.client ServerProxy:xmlrpc.'
'server SimpleXMLRPCServer:re search').split(":"):
 exec('from {0} import {1}'.format(x.split()[0],','.join(x.split()[1:])))
# Above codeblock equivalent to:
#from itertools import takewhile, count
#from os.path import exists
#from hashlib import sha256
#from time import time, ctime
#from json import dump, load, dumps, loads
#from sys import argv
#from xmlrpc.client import ServerProxy
#from xmlrpc.server import SimpleXMLRPCServer
#from re import search
# Globals and aliases
PW,Sp,SS,SV='001',ServerProxy,SimpleXMLRPCServer,lambda x:x.serve_forever()

# Transform a message list as a pretty message.
r=lambda m:"@{}\t- on {}: {}".format(m[1],ctime(m[0])[:16],m[2])

# Give the hash of a message list.
H=lambda m:sha256(bytes(dumps(m),'utf8')).hexdigest()

# Generate a new message list and do Proof-Of-Work using a hash-checking integer-generator.
# This creates a lambda function that takes a list and appends a nonce that makes
# for a good hash.. and then calls the function to return the list with that nonce
# appended. So, it generates a full message on the fly which can be thereafter
# treated as a native list.

# This pair of functions allows easy creation and proof-of-working on messages
# with a single function call. In effect it takes a name and message, creates
# a partial message consisting of [time(), name, message] and passes it to a
# lambda function that appends the first integer found which creates a hash
# below the proof-of-work threshold.
GetNonce=lambda O,n:takewhile(lambda x:H(O[:3]+[x])>n,count())
M=lambda n,m:(lambda O:O+[[n+1 for n in GetNonce(O,PW)].pop()])([time(),n,m])

# Load DB on script launch, and shortcut for saving current DB to file.
DB,Sav=load(open("D"))if exists("D")else[[],[],[]],lambda:dump(DB,open("D","w"))

# Add things to list only if new, save global database, return list.
Z=lambda d,n:d.extend([x for x in n if x and x not in d]) or Sav() or sorted(d)

# Alias the above to handle Stream, Followers, and Peers sublists of database.
S,F,P=lambda n=[]:(Z(DB[2],n)),lambda n=[]:(Z(DB[1],n)),lambda n=[]:(Z(DB[0],n))

# Search the stream for keywords as regex.
G=lambda g='':[x for x in filter(lambda n:(g=='')or search(g,r(n)),S())]
# Perform multiple concurrent searches of the stream:
R=lambda l:sorted([x for y in [G(z) for z in l] for x in y])
# The above is equivalent to:
# def R(l):
#  Output = []
#  # Remembering that G(z) will return a list of matches.
#  for ResultsSubList in [G(z) for keyword in l]:
#   for x in ResultsSubList:
#    Output.append(x)
#  return sorted(Output)

# AM is a one-way version of "S" that adds msgs with an OK length and hash & returns "1".
# "or 1) and 1" means "always return 1 regardless of outcome".. i.e. don't return
# entire stream to a peer whenever they post a message, wait for them to ask for
# their follows list or regex search!
# MessageOK checks: Is Hash value below proof of work threshold?
# If so, is message field at most 151 characters?
# If so, is user ID at most 25 characters? (Stop people gaming the system!)
MessageOk = lambda x: H(x)<=PW and len(x[2])<151 and len(x[1])<25
AM=lambda NM:(S([(NM if MessageOk(NM) else [])])or 1)and 1

# U is only used in server mode. It uses [2:3] and [3:4] slicing to get args [2] and [3],
# respectively, but calling ranges in this way avoids indexerrors when these args aren't given.
# Md is "Mode", and is the first letter of the first argument.
U,Md="http://"+''.join(argv[2:3])+":"+''.join(argv[3:4]),argv[1][0]

# f takes mode n and argument(s) a.
# a should always be a list, for starters.
# n==0 => Share peer list: Send known peers to server, server returns updated known list.
# n==1 => Share known message list: Offer new messages to server which keeps them if proof-of-work is sufficient.
# n==2 => Search for matches: Send a list of regex patterns, server returns all matching messages.
f=lambda n,a:(n<1 and P(a))or(n==1 and AM(a))or(n==2 and R(a))

# == Debug only ==
# df = debug f, here to test only.
def df(n,a):
  print("Request:",n,a)
  result= 'Error'
  try:
   result = f(n,a)
  except Exception as E:
   print("Exception while handling args for mode",n,":",E)
  print("Response:",result)
  return result

# Server: TinyStatus.py serve hostname portnum [otherhosts...]
# AddFollow: TinyStatus.py addfollow [follow1 follow2 ...]
# UnFollow: TinyStatus.py unfollow [follow1 follow2 ...]
# Post: TinyStatus.py post server username message
# Find: TinyStatus.py find [search1 search2 ...]
# Update: TinyStatus.py update server
# Technically the commands can be shortened to the first character only.

if Md == "s":
  # Don't ask self for a server list because self has not yet started server.
  # Otherwise, update P() with the output from sending known servers (including self)
  # to the remote server Sr.
 try: P( [ x for Sr in P(argv[4:]) if Sr!=U for x in Sp(Sr).f(0,DB[0]+[U]) ] )
 except Exception as E: print("Error while bootstrapping servers:",E)
 # Start server with lambda using terminal-provided hostname and port values.
 (lambda E:E.register_function(df,"f") or SV(E))(SS(("localhost",int(argv[3]))))
elif Md in "ar":
 # C is a disposable variable and is probably not even necessary to make this work.
 C=F(argv[2:]) if Md=="a" else [DB[1].remove(x) for x in argv[2:] if x in F()]
elif Md in "puf":
 # In post mode, offer a prompt for the message and use username given at Terminal.
 # In other modes, make an empty list instead; server will ignore this.
 # In post or update mode, send list of follows to server to update local stream.
 # In find mode, send list of arguments after the target server as "find" strings.
 NM,Ft = M(argv[3],input(">")) if Md=='p' else[], argv[3:] if Md=="f" else DB[1]
 # Can I compress this three-liner into two with a nested for expression? O_o
 for Url in Sp(argv[2]).f(0,DB[0]+argv[2:3]):
  try: Sp(Url).f(1,NM) and [AM(x) for x in Sp( Url ).f( 2, Ft )]
  except Exception as E: print("Error communicating with peer '",Url,"':",E)

 # Fetches Stream (which is sorted on the fly above) and prints prettified messages.
 print('\n'.join([r(x) for x in S()]))
