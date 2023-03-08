1. In a terminal: nc edu-ctf.zoolab.org 10104
2. copy the given number to factordb
3. In getgenerator.py
	set p = the prime we got from the server
	set factor = the small factor we got on factordb
4. Run: python3 getgenerator.py
5. Paste the generator to terminal
6. Copy the returned ciphertext
7. In findflag.py
	set p = the prime we got from the server
	set g = our generator
	set ciphertext = the ciphertext returned by the server
	set the factor = the small factor we got on factordb
8. Run: python3 findflag.py
	
