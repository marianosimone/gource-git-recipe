import urllib, hashlib

def download(email, filename, size):
    gravatar_url = "http://www.gravatar.com/avatar/{hash}?size={size}".format(hash=hashlib.md5(email.lower()).hexdigest(), size=size)
    urllib.urlretrieve(gravatar_url, filename=filename)
