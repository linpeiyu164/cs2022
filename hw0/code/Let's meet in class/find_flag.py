from Crypto.Util.number import long_to_bytes
a = 591
b = 1516
c = 2849
d = 3451
e = 4668

exp = 65537
p = 92017932396773207330365205210913184771249549355771692523246399384571269833668487945963934319507538171501041280674304304879328757539798699280378034748542218248740777575679398093116579809607067129824965250071416089841516538588253944223235904445546895574651603636188746948921937704060334290364304972412697492577
enc = 87051682992840829567429886737255563980229964191963649650455667117285375334750716083826527488071966389632402954644144719710970265754062176648776448421065665281172133368294041777397049228273163978348132440822019295870429065335674151133125629968366491582233750452365390672536361224322642295053741696809519283644

a = pow(a, 65537, p)
b = pow(b, 65537, p)
c = pow(c, 65537, p)
d = pow(d, 65537, p)
e = pow(e, 65537, p)

mul = (a * b * c * d * e) % p
mul = pow(mul, -1, p)
enc = (enc * mul) % p
flag = long_to_bytes(enc)
print(flag)