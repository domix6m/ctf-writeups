import sys, struct
from unicorn import *
from unicorn.x86_const import *
BIN="/home/parallels/Downloads/rev_[medium]-leftover-sample/chall"
d=open(BIN,'rb').read()
def run(inp, trace=False, verbose=False, hooks=None):
    mu=Uc(UC_ARCH_X86,UC_MODE_32)
    mu.mem_map(0x08048000, 0x8823000-0x08048000)  # covers text,data,bss
    mu.mem_write(0x08048000, d[:0x31020])
    mu.mem_write(0x08079020, d[0x31020:0x31020+0x5a947c])
    mu.mem_map(0xff000000,0x100000)  # stack
    mu.mem_map(0x10000000,0x1000000) # heap
    heap=[0x10000000]
    STDIN,STDOUT=0x086224a0,0x086224a4
    mu.mem_write(STDIN,struct.pack('<II',0x11110000,0x22220000))
    esp=0xff0ff000
    mu.reg_write(UC_X86_REG_ESP,esp)
    out=bytearray(); inbuf=[inp]
    st={'n':0,'done':False,'pc':0x804908c}
    def u32(a): return struct.unpack('<I',mu.mem_read(a,4))[0]
    def cstr(a):
        s=b''
        while True:
            c=mu.mem_read(a,1)
            if c==b'\0':return s
            s+=bytes(c);a+=1
    def fmt(f,args):
        # minimal printf
        import re
        res=b'';i=0;ai=0
        while i<len(f):
            if f[i:i+1]==b'%':
                m=re.match(rb'%([-0 #+]*)(\d*)(l*)([dsxuc%])',f[i:])
                spec=m.group(4)
                if spec==b'%':res+=b'%'
                else:
                    v=args(ai);ai+=1
                    if spec==b's':res+=cstr(v)
                    elif spec==b'c':res+=bytes([v&0xff])
                    elif spec==b'd':res+=str(struct.unpack('<i',struct.pack('<I',v))[0]).encode()
                    elif spec==b'u':res+=str(v).encode()
                    elif spec==b'x':res+=('%x'%v).encode()
                i+=len(m.group(0))
            else: res+=f[i:i+1];i+=1
        return res
    def ext(name):
        sp=mu.reg_read(UC_X86_REG_ESP); ret=u32(sp); a=lambda k:u32(sp+4+4*k)
        r=0
        if name=='sigaction': r=0
        elif name=='printf':
            s=fmt(cstr(a(0)),lambda k:a(k+1)); out.extend(s); r=len(s)
        elif name=='fflush': r=0
        elif name=='fgets':
            buf,n=a(0),a(1); data=inbuf[0][:n-1]
            if b'\n' in data: data=data[:data.index(b'\n')+1]
            inbuf[0]=inbuf[0][len(data):]
            if not data: r=0
            else: mu.mem_write(buf,data+b'\0'); r=buf
        elif name=='malloc':
            r=heap[0]; heap[0]+= (a(0)+15)&~15
        elif name=='free': r=0
        elif name=='exit':
            st['done']=True; mu.emu_stop(); return
        if verbose: print('CALL',name,hex(ret),hex(a(0)),hex(r),file=sys.stderr)
        mu.reg_write(UC_X86_REG_EAX,r)
        mu.reg_write(UC_X86_REG_ESP,sp+4)
        mu.reg_write(UC_X86_REG_EIP,ret)
    plt={0x8049010:'fgets',0x8049020:'free',0x8049030:'sigaction',0x8049040:'fflush',0x8049050:'printf',0x8049060:'malloc',0x8049070:'exit'}
    def hk(mu,addr,size,u):
        if addr in plt: ext(plt[addr])
        elif addr==0x807705e:
            st['n']+=1
            mu.reg_write(UC_X86_REG_EIP,0x8049107)
    for a in plt: mu.hook_add(UC_HOOK_CODE,hk,begin=a,end=a)
    mu.hook_add(UC_HOOK_CODE,hk,begin=0x807705e,end=0x807705e)
    if trace:
        def wh(mu,acc,addr,size,val,u):
            print("W",hex(mu.reg_read(UC_X86_REG_EIP)),hex(addr),size,hex(val%(1<<(8*size))),file=sys.stderr)
        mu.hook_add(UC_HOOK_MEM_WRITE,wh,begin=0x10000000,end=0x10ffffff)
        def rh(mu,acc,addr,size,val,u):
            print("R",hex(mu.reg_read(UC_X86_REG_EIP)),hex(addr),size,hex(int.from_bytes(mu.mem_read(addr,size),'little')),file=sys.stderr)
        mu.hook_add(UC_HOOK_MEM_READ,rh,begin=0x10000000,end=0x10ffffff)
        mu.hook_add(UC_HOOK_MEM_READ,rh,begin=0x8622528,end=0x8622528+0x200)
        mu.hook_add(UC_HOOK_MEM_WRITE,wh,begin=0x8622610,end=0x8622700)
    if hooks: hooks(mu)
    pc=0x804908c
    while not st['done']:
        try:
            mu.emu_start(pc,0)
            break
        except UcError as e:
            if e.errno in (UC_ERR_WRITE_UNMAPPED,UC_ERR_READ_UNMAPPED):
                pc=0x8049080
            else:
                print('ERR',e,hex(mu.reg_read(UC_X86_REG_EIP)),file=sys.stderr);break
    st["heap"]=bytes(mu.mem_read(0x10000000,heap[0]-0x10000000)); st["mu"]=mu
    return bytes(out), st
if __name__=='__main__':
    o,n=run(sys.argv[1].encode()+b'\n',verbose=True)
    print(o.decode(errors='replace')); print('loops',n)
