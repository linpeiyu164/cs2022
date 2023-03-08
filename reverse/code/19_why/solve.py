# Run: python3 solve.py

from Crypto.Util.number import long_to_bytes

enc_flag= 0x50564B51857378737E697073787369777A7C797E6F6D7E2B87
flag = long_to_bytes(enc_flag)
flag = bytearray(flag)
for i in range(len(flag)):
    flag[i] -= 10
flag = bytes(flag)
print(flag)

# FLAG{init_fini_mprotect!}
# Edit -> patch program -> change byte

'''
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int i; // [rsp+Ch] [rbp-4h]

  printf("Give me flag: ");
  __isoc99_scanf("%25s", flag);
  for ( i = 0; i <= 24; ++i )
  {
    if ( flag[i] + 10 != enc_flag[i] )
      return 0;
  }
  pass = 1;
  return 0;
}
'''