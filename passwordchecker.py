#Password Checker Project
from asyncore import read
import requests
import hashlib
import sys

"""
Visit the README.md for full documentation of this project,
but basically, this project checks a password if it has been hacked or not
and it uses the Hash1 level of hashing in securing the password.
"""

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res
#print(res)

#def read_res(response):
    #print(response.text)
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0
        #print(h, count)
    print(hashes)

def pwned_api_check(password):
    #print(hashlib.sha1(password.encode('utf-8')).hexdigest().upper())
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    #print(first5_char, tail)
    #print(response)
    #return read_res(response)
    return get_password_leaks_count(response, tail)
#pwned_api_check('123')
#request_api_data('123')

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times.... You\'d better change your password')
        else:
            print(f'{password} was not found. Carry on!.')
    return 'done'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))