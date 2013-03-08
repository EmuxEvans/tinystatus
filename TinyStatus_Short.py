for x in ('itertools takewhile count:os.path exists:hashlib sha256:time time ct'
'ime:json dump dumps load loads:sys argv exit:xmlrpc.client ServerProxy:xmlrpc.'
'server SimpleXMLRPCServer:re search').split(":"):
 exec('from {0} import {1}'.format(x.split()[0],','.join(x.split()[1:])))
PW,Sp,SS,SV='001',ServerProxy,SimpleXMLRPCServer,lambda x:x.serve_forever()
r=lambda m:"@{}\t- on {}: {}".format(m[1],ctime(m[0])[:16],m[2])
H=lambda m:sha256(bytes(dumps(m),'utf8')).hexdigest()
GetNonce=lambda O,n:takewhile(lambda x:H(O[:3]+[x])>n,count())
M=lambda n,m:(lambda O:O+[[n+1 for n in GetNonce(O,PW)].pop()])([time(),n,m])
DB,Sav=load(open("D"))if exists("D")else[[],[],[]],lambda:dump(DB,open("D","w"))
Z=lambda d,n:d.extend([x for x in n if x and x not in d]) or Sav() or sorted(d)
S,F,P=lambda n=[]:(Z(DB[2],n)),lambda n=[]:(Z(DB[1],n)),lambda n=[]:(Z(DB[0],n))
G=lambda g='':[x for x in filter(lambda n:(g=='')or search(g,r(n)),S())]
R=lambda l:sorted([x for y in [G(z) for z in l] for x in y])
MessageOk = lambda x: H(x)<=PW and len(x[2])<151 and len(x[1])<25
AM=lambda NM:(S([(NM if MessageOk(NM) else [])])or 1)and 1
U,Md="http://"+''.join(argv[2:3])+":"+''.join(argv[3:4]),argv[1][0]
f=lambda n,a:(n<1 and P(a) or [U])or(n==1 and AM(a))or(n==2 and R(a))
if Md == "s":
 try: P( [ x for Sr in P(argv[4:]) if Sr!=U for x in Sp(Sr).f(0,DB[0]+[U]) ] )
 except Exception as E: print("Error while bootstrapping servers:",E)
 (lambda E:E.register_function(f,"f") or SV(E))(SS((argv[2],int(argv[3]))))
elif Md in "ar":
 C=F(argv[2:]) if Md=="a" else [DB[1].remove(x) for x in argv[2:] if x in F()]
elif Md in "puf":
 NM,Ft = M(argv[3],input(">")) if Md=='p' else[], argv[3:] if Md=="f" else DB[1]
 for Url in Sp(argv[2]).f(0,DB[0]+argv[2:3]):
  try: Sp(Url).f(1,NM) and [AM(x) for x in Sp( Url ).f( 2, Ft )]
  except Exception as E: print("Error communicating with peer '",Url,"':",E)
 print('\n'.join([r(x) for x in S()]))
