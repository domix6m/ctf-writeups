import sys; sys.path.insert(0,'.')
import keys, hashlib
d=open("/home/parallels/Downloads/rev_[medium]-leftover-sample/chall",'rb').read()
tab=d[0x31020:0x31048]; target=d[0x31048:0x31068]
p=b''
for i in range(40):
    k,_=keys.get(p+b'\n')
    p+=bytes([tab[i]^k[i]])
print(p)
print(hashlib.sha256(p).hexdigest()==target.hex(), hashlib.sha256(p).hexdigest(), target.hex())
k,o=keys.get(p+b'\n'); print(o)
