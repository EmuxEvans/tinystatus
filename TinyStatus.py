#!/usr/bin/env python3
for x in ('itertools takewhile count:os.path exists:hashlib sha256:time time ct'
'ime:json dump dumps load loads:sys argv:xmlrpc.client ServerProxy:xmlrpc.serve'
'r SimpleXMLRPCServer:re search').split(":"):
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

# If you're looking for global defines like POW, SA and such, they're embedded
# in the object code, as they won't be required until instantiation and it saves
# space.

if not exists("sd"):(lambda f:(dump([[],[],[]],f),f.close()))(open("sd",'w'))
# Now can forego testing for file existence later, which requires multiple lines

# O is "output", dumps [[Peers],[follows],[messages]] to file "sd".
# Setting Class attribute M to empty dict allows instances to just assume it's there, avoiding attributeerrors.
# Because instance self.M is set in init after first use of self.A, it's no longer referring to the class attribute.
class D:O,M=lambda s:dump([s.P,s.F,[s.M[m].r() for m in s.M]],open("sd","w")),{}
# Init sets s.P to Peers, s.F to follows, calls s.A([]) to regenerate message dict and pass to s.M.
def Di(s,B): s.P,s.F,s.M=B[0],B[1], s.A([M(x[1],x[2],x[0],x[3]) for x in B[2]])
# A returns a dict of message hashes:messages, if they show proof of work.
# It does this by converting the existing s.M dict into a list of [key,value] pairs,
# and adds this to the new proposed list of [key,value] pairs, then processes them all.
# This would be pretty inefficient for large dicts!
SA,A=setattr,lambda s,L:dict([[m.H(),m]for m in L+[s.M[k]for k in s.M]if m.H()<POW])
# Why doesn't D.a(L) return D.A(L) as instructed by the "and" bit?
D.A,D.__init__,D.a=A,Di,lambda s,L:SA(s,"M",s.A(L)) and s.A(L)
# This method should return a dictionary that is a combination of s.M and new messages in a list.
# Message list can be a property that generates sorted messages from this dict on the fly (use property() function)
D.S=property(lambda s:sorted([s.M[m] for m in s.M]))
# Search DB by regex!
D.G=lambda s,g=0:[x for x in filter(lambda n:(g==0)or search(g,str(n)),s.S)]

class M:N,r=lambda s,x:SA(s,'v',x),lambda s,x=0:[s.t,s.n,s.m[:150],x or s.v]
def mi(s,n,m,t=0,v=0):s.t,s.n,s.m,s.v=t or time(),n,m[:150],v # Msg Format: [time,nick,msg,nonce]
def mH(s,n=0):return sha256(bytes(dumps(s.r(n)),'utf8')).hexdigest()
# POW is proof of work threshold, defined here just to save space!
Rs,POW,M.H,M.__init__="@{}, on {}: {}","0001",mH,mi
M.__lt__,M.__repr__=lambda s,o:s.t<o.t,lambda s:(Rs).format(s.n,ctime(s.t),s.m)
M.P=lambda s:[s.N(x+1) for x in takewhile(lambda x:s.H(x)>POW,count())].pop()
# Must be x+1 as takewhile doesn't give the last, working number. pop() at end prevents returning as value is None.

DB=D(loads(open("sd")))

# Usage similar to TinyP2P:
# $ python3 tinystatus server <external ip or hostname> <portnum> <otherservers...>
# Poll fetches messages from remote servers and prints them.
# $ python3 tinystatus update <servers...>
# $ python3 tinystatus post "message" <servers..>
# Follow is not just for people: you follow regexes! Names come first though, so to follow a person: follow "@onetruecathal"
# $ python3 tinystatus follow <stuff..>
# $ python3 tinystatus rmfollow <stuff..>
# $ python3 tinystatus search <string> <servers..>
