import os, sys, socket, re, random, ssl

from sys import version_info
PY3K = version_info >= (3, 0)

if PY3K:
    import urllib.request as urllib
    import http.cookiejar as cjar
else:
    import urllib2 as urllib
    import cookielib as cjar


def fetch(server):
        '''
        This function gets your IP from a specific server.
        '''
        url = None
        cj = cjar.CookieJar()
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        opener = urllib.build_opener(urllib.HTTPCookieProcessor(cj), urllib.HTTPSHandler(context=ctx))
        opener.addheaders = [('User-agent', "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"),
                             ('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                             ('Accept-Language', "en-US,en;q=0.5")]

        try:
            url = opener.open(server, timeout=4)
            content = url.read()

            # Didn't want to import chardet. Prefered to stick to stdlib
            if PY3K:
                try:
                    content = content.decode('UTF-8')
                except UnicodeDecodeError:
                    content = content.decode('ISO-8859-1')

            m = re.search(
                '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',
                content)
            myip = m.group(0)
            return myip if len(myip) > 0 else ''
        except Exception:
            return ''
        finally:
            if url:
                url.close()

def get_ext():
        '''
        This function gets your IP from a random server
        '''
	server_list = ["http://ip.dnsexit.com",
                       "http://ifconfig.me/ip",
                       "http://ipecho.net/plain"]

        myip = ''
        for i in range(7):
            myip = fetch(random.choice(server_list))
            if myip != '':
                break
        return myip

if __name__ == '__main__':
    print(get_ext())
