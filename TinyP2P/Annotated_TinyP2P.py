# tinyp2p.py 1.0 (C) 2004, E.W. Felten, License: Creative Commons BY-NC-SA 2.0
# doc: web.archive.org/web/20070927205613/www.freedom-to-tinker.com/tinyp2p.html
import sys, os, SimpleXMLRPCServer, xmlrpclib, re, hmac
ar,pw,res = (sys.argv,lambda u:hmac.new(sys.argv[1],u).hexdigest(),re.search)
pxy,xs = (xmlrpclib.ServerProxy,SimpleXMLRPCServer.SimpleXMLRPCServer)

# If p, then use p as a regular expression to search current directory contents.
# Else, list all directory contents.
def ls(p=""):return filter(lambda n:(p=="")or res(p,n),os.listdir(os.getcwd()))

if ar[2]!="client":
  # Server code: Usage python tinyp2p.py password "server" hostname portnum [otherurl]
  # Uses [otherurl] to join network of servers!
  # myU = This server URL, prs = Other server URLs, function srv = serve x forever.
  myU,prs,srv = ("http://"+ar[3]+":"+ar[4], ar[5:],lambda x:x.serve_forever())

  # Returns prs with no args, or prs with x new values if x given (permanent change).
  # This seems to work because of a list comparison quirk;
  #  [1] or [2] yields [1], because [1] evals true and this idiom is used for default assignments.
  #  [1] and [2] yields [2], not True or [1,2] or ([1],[2])
  # A list full of "None" still evals True, but for this to return prs even with
  # no x, the "[y in prs or prs.append(y) for y in x]" bit isn't enough, it needs
  # to be coupled with "or 1". However, the internal brackets are unnecessary,
  # so this works as:
  # def pr(x=[]): return ([y in prs or prs.append(y) for y in x] or 1) and prs
  def pr(x=[]): return ([(y in prs) or prs.append(y) for y in x] or 1) and prs

  # Bracket spacing helps make this more comprehensible:
  #    func(f) read/close f -> (contents,int/None),
  #                                      Call with open file(n)
  #                                                         return first value (file contents)
  #  ( ( lambda f: ( f.read(), f.close() ) )( file(n) ) )[0]
  # in Python 3, this is easier but requires line breaks.
  # def c(n):
  #  with file(n) as f:
  #   return f.read()
  # But this c construction still works in py3k with "open" instead of "file".
  def c(n): return ((lambda f: (f.read(), f.close()))(file(n)))[0]

  # p,n,a
  # -> p = server url, hmac'd with password. Authentication string.
  # -> n = function mode: 0 = ?, 1 = search, 2+ = download
  # -> a = in search mode, the search string. In Download mode, the filename.
  # (p==pw(myU))
  # -> Checks if p equals hmac(MyUrl,Password), short-circuits otherwise.
  # ( ( ( n==0 ) and pr( a ) ) or ( (n==1) and [ls(a)] ) or c(a) )
  # -> Short-circuits again; functions as a simple if/elif/else:
  #  if ( p == pw(myU) ):
  #    if ( n == 0 ) and pr(a): lambda returns server list including any new servers given as "a".
  #    elif ( n == 1 ) and [ls(a)]: lambda returns a list of files matching "a".
  #    else: c(a): returns file contents of a.
  # Example usages from client mode:
  # f(pw(serverurl),0,[]) -> returns urls of servers in network.
  # f(pw(serverurl),0,[myU]) -> registers myU on server and gets resulting known-servers list.
  # (f(pw(serverurl),1,ar[4]))[0] -> returns list of filenames on servers
  # f(pw(serverurl),2,fn) -> Fetches file contents for direct file writing
  f=lambda p,n,a:(p==pw(myU))and(((n==0)and pr(a))or((n==1)and [ls(a)])or c(a))

  # Below functions aren't called by server or referred to by f, so must
  # be setup functions prior to server initialisation:

  # If u is this server's URL AND prs is not empty, return pr().
  # Else, call the server's f function to return a server list, plus
  # local server's set of URLs (remote server keeps these URLs, too)
  # This is basically a version of "pr()" that works equally on local or
  # remote servers.
  def aug(u): return ((u==myU) and pr()) or pr(pxy(u).f(pw(u),0,pr([myU])))

  # "pr() and" idiom means the following code only runs if pr() is true, i.e.
  # alt servers are known/given at terminal invocation.
  # If it runs, it calls the first server in pr() for its server list,
  # and for each server returned in that server's pr() list, it calls
  # for *that* server's server list. All results are added to local prs.
  # Only the first server returned from pr() is used, because the contents
  # of pr() are called and sent to remote server when calling aug() and are
  # therefore returned; in other words, it would be redundant to use the
  # whole output of pr()!
  pr() and [aug(s) for s in aug(pr()[0])]

  # Because of the "this or other" idiom, as register_function returns None,
  # it is called and then the interpreter tries calling srv(sv).
  # Neither returns anything becuse srv(sv) immediately starts serving the
  # argument ( xs(hostname, port) ) immediately, blocking the script from here
  # onwards until closed with ctrl-c.
  (lambda sv:sv.register_function(f,"f") or srv(sv))(xs((ar[3],int(ar[4]))))

# Client code. Never runs in server mode because server blocks script when
# initialised.
# Usage python tinyp2p.py password "client" serverurl pattern
#  api for servers: server.f( (pw-hmac'd server URL), (mode), (searchstring or filename) )
#  where modes are:
#   0([newservers])->server list.extend(newservers),
#   1(search_string)->filename list
#   x(file_name)->Download file (where x is anything but 0 or 1)
for url in pxy(ar[3]).f(pw(ar[3]),0,[]):
  # For each filename that is NOT in current directory, :
  for fn in filter(lambda n:not n in ls(), (pxy(url).f(pw(url),1,ar[4]))[0]):
    (lambda fi:fi.write(pxy(url).f(pw(url),2,fn)) or fi.close())(file(fn,"wc"))
