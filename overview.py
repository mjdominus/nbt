#!/usr/bin/python3
from nbt import nbt

from sys import argv

def dump(f, depth=0, prefix="| "):
    i = prefix * depth
    for k, v in f.items():
        print(f'{prefix * depth}{k}:', end=" ")
        recurse = False
        try:
            v.items()
            recurse = True
        except AttributeError:
            pass
        if recurse:
            print('')
            dump(v, depth+1)
        else:
            if len(str(v)) < 100:
                print(f'{v}')
            else:
                print(f'<{len(str(v))} bytes data>')
            

for file in argv[1:]:
    dump(nbt(file=file).contents)
    


