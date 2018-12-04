# Simple CGI Redirect for TemaTres API

This repository has a simple [Python CGI script](https://wiki.python.org/moin/CgiScripts) to get a search term code and redirect it to the correspondent page in TemaTres. I'm running this under a Dreamhost machice and I've followed [this tutorial](https://help.dreamhost.com/hc/en-us/articles/217297307-CGI-overview) to enable it. Because of that, I'm using Python 2.7 instead of Python 3.

To run this script on your own server you must:

1. On the server side, install [requests Python lib]() with the command `pip install requests`
2. Copy the `tematres_api.py` to your server's cgi directory. You can do as following:

```
scp tematres_api.py user@myserver.com:/home/user/mysite.com/public/cgi-bin/tematres_api.py
```

After doing that, you proably should be able to access the script by accessing `http://mysite.com/cgi-bin/tematres_api.py?term_code=dat.var`, for example.
