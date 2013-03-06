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
A=lambda s,L=[]:dict([[m.H(),m]for m in L+[s.M[k]for k in s.M]if m.H()<POW])
# Why doesn't D.a(L) return D.A(L) as instructed by the "and" bit?
SA,D.A,D.__init__,D.a=setattr,A,Di,lambda s,L:SA(s,"M",s.A(L)) and s.A(L)
# Message list method that generates sorted messages from hash dict on the fly: primary "stream" method.
# Turned this into a message fetcher, too; if hl is provided, only hashes within the hl list are returned (Hopefully!)
# Below; tried to hack in a save during message stream getting.
D.S=lambda s,hl=[]:(s.O() or sorted([s.M[m] for m in s.M if m in (hl or s.M)]))
#D.S=lambda s,hl=[]:sorted([s.M[m] for m in s.M if m in (hl or s.M)])
# Search DB by regex! "G" is for "Get"
D.G=lambda s,g=0:[x for x in filter(lambda n:(g==0)or search(g,str(n)),s.S())]
# Need handlers for Servers; this adds & returns current list.
# def pr(x=[]): return ([(y in prs) or prs.append(y) for y in x] or 1) and prs
D.p=lambda s,n=[]:([(y in s.P) or s.P.append(y) for y in n] or 1) and s.P
# Can't keep track of which servers are good and bad, as it'd lead to different entries between peer servers:
# the assessment metadata would lead to servers accepting duplicates of known servers thinking them unique because
# of peer markup.
# Instead, we'll pop and insert(0, foo) foo when it is successfully reached, so that successful peers
# are always tried first.
# So, a method that code can call back to the database to say "this server worked": (Pr=Peer Recommend)
# Finds, pops and inserts peer into first position in peer list.
# NB: So far this is nowhere in use.
D.Pr=lambda s,n:s.P.insert(s.P.pop(s.P.index(n)))

class M:N,r=lambda s,x:SA(s,'v',x),lambda s,x=0:[s.t,s.n,s.m[:150],x or s.v]
def mi(s,n,m,t=0,v=0):s.t,s.n,s.m,s.v=t or int(time()),n,m[:150],v # Msg Format: [time,nick,msg,nonce]
def mH(s,n=0):return sha256(bytes(dumps(s.r(n)),'utf8')).hexdigest()
# POW is proof of work threshold, defined here just to save space!
Rs,POW,M.H,M.__init__="@{}, on {}: {}","001",mH,mi
M.__lt__,M.__repr__=lambda s,o:s.t<o.t,lambda s:(Rs).format(s.n,ctime(s.t),s.m)
M.P=lambda s:[s.N(x+1) for x in takewhile(lambda x:s.H(x)>POW,count())].pop()
# Must be x+1 as takewhile doesn't give the last, working number. pop() at end prevents returning as value is None.

DB,SP=D(load(open("sd"))),ServerProxy
I,SXS=lambda L:SA(DB,'M',DB.A([M(x[1],x[2],x[0],x[3]) for x in L])),SimpleXMLRPCServer
# s usage:
# s(0,a): returns DB.p(a) => Appends peer list a and returns full peer list. --> Works!
# s(1,a): returns DB.G(a) => Returns list of hashes for messages matching regex a.
# s(2,a): returns DB.S(a) => Returns list of messages whose hashes are in list a, OR all messages in stream if a empty.
# s(3+,a): calls I(a) (=>DB.A(a) with message instantiation) and returns DB.O() (Which saves the current DB)
s=lambda n,a:((n<1 and DB.p(a))or(n==1 and DB.G(a))or(n==2 and DB.S(a))or(I(a)) and DB.O())
# Usage similar to TinyP2P:
# $ python3 tinystatus server <external ip or hostname> <portnum> <otherservers...>
# Poll fetches messages from remote servers and prints them.
# $ python3 tinystatus update <servers...>
# $ python3 tinystatus post "name" "message" <servers..>
# Follow is not just for people: you follow regexes! Names come first though, so to follow a person: follow "@onetruecathal"
# $ python3 tinystatus follow <stuff..>
# $ python3 tinystatus unfollow <stuff..>
# $ python3 tinystatus search <string> <servers..>
print(argv)
if "serve" in argv[1].lower():
 # TinyP2P Server Bootstrap:
 # myU,prs,srv = ("http://"+ar[3]+":"+ar[4], ar[5:],lambda x:x.serve_forever())
 # def aug(u): return ((u==myU) and pr()) or pr(pxy(u).f(pw(u),0,pr([myU])))
 # pr() and [aug(s) for s in aug(pr()[0])]

 # Database has a "P" key for peers, instead of a floating "prs" variable, and "p" method identical to pr()
 U,P,sv="http://"+argv[2]+":"+argv[3],DB.p(argv[4:]),lambda x:x.serve_forever()
 #f=lambda p,n,a:(p==pw(myU))and(((n==0)and pr(a))or((n==1)and [ls(a)])or c(a))
 # n=mode: mode 0 is fetch peers, mode 1 is fetch hashes by keyword, mode 2 is fetch messages by hash list.
 # Mode 3+ means "post".
 # Will this die the server? Do we need an aux?
 if argv[4:]: foo=[DB.p(SP(x).s(0,D.p())) for x in D.p()[:]]
 #(lambda sv:sv.register_function(f,"f") or srv(sv))(xs((ar[3],int(ar[4]))))
 DB.p([U])
 (lambda E:E.register_function(s,"s") or sv(E))(SXS((argv[2],int(argv[3]))))
elif argv[1][:3] == "fol": DB.F.extend(argv[2:])
elif "unf" in argv[1]: foo=[DB.F.remove(x) and DB.O() for x in argv[2:]]
elif "post" in argv[1]:
 # Use list iteration to accomplish message creation, Proof-of-work and json export.
 #MyMsg = [x.P() and x.r() for x in [M(argv[2],argv[3])]].pop()
 MyMsg = M(argv[2],argv[3])
 MyMsg.P()
 MyMsg = MyMsg.r()
 print(MyMsg)
 for url in SP(argv[4]).s(0,DB.p()):
  SP(url).s(3,MyMsg)
else:
 print("Stream mode")
 for url in SP(argv[1]).s(0,DB.p()):
  # For each followed keyword/user/search:
  # Get list of matching hashes, and if it's not a known hash, append to a list,
  # then dump the list in a message request by hash to the server.
  for kw in DB.F: print(kw)
  for kw in DB.F: DB.A(SP(url).s(2,[x for x in SP(url).s(1,kw)if x not in DB.M]))
 print(DB.S())
DB.O()
