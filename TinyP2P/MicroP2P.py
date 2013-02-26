# This is a python 3 version of TinyP2P, crammed into even less space. Not yet working.
for x in ('import sys,os,xmlrpc.server as S,xmlrpc.client as C,re,hmac;ar,pw,re'
's=sys.argv,{l} u:hmac.new(sys.argv[1],u).hexdigest(),re.search;pxy,xs=(C.Serve'
'rProxy,S.SimpleXMLRPCServer);def ls(p=""):{r} filter({l} n:(p=="")or res(p,n),'
'os.listdir(os.getcwd()));def pr(x=[]):{r}([(y in prs)or prs.append(y) for y in'
' x]or 1)and prs;def c(n):{r}(({l} f:(f.read(),f.close()))(open(n),"rb"))[0];f='
'{l} p,n,a:(p==pw(myU))and(((n==0)and pr(a))or((n==1)and[ls(a)])or c(a));def au'
'g(u):{r}((u==myU)and pr())or pr(pxy(u).f(pw(u),0,pr([myU])));if ar[2]!="client'
'":; myU,prs,srv="http://"+ar[3]+":"+ar[4],ar[5:],{l} x:x.serve_forever(); pr()'
'and[aug(s) for s in aug(pr()[0])]; ({l} sv:sv.register_function(f,"f")or srv(s'
'v))(xs((ar[3],int(ar[4]))));for u in pxy(ar[3]).f(pw(ar[3]),0,[]):; for N in f'
'ilter({l} n:not n in ls(),(pxy(u).f(pw(u),1,ar[4]))[0]):;  ({l} w:w.write(pxy('
'url).f(pw(url),2,fn))or w.close())(open(N,"wb"))'
).format(l='lambda',r='return').split(";"):exec(x)
