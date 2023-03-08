Run : python3 guess.py

- guess.py : sends slightly modifed versions of script to the server repeatedly to guess flag2 byte by byte.
- script : This file is not used, but I included it for readability purposes.
(In guess.py, script is stored as a multi-lined string which makes it difficult to read)
(In guess.py, we need to change the variable cguess at the top, and also change the index of flag2 to guess each character independently.)

Logic in guess.py:

flg = ""
for i in 50                             # >= len(flag2)
    include i in script
    for c in range(33, 128)     # guess the characters
        include c in script
        res = send_http_request()
        check res == old_flag:
            flg += character
            print(flg)
            break;