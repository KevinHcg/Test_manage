from sgin.test import *
import json
d=gps_list()
print(d)
print({'a:': d })

x={'a':d}
print(type(x))
g= str(x).replace("\\\\","\\")
print(g)
print(type(g))


import ast
t=ast.literal_eval(g)
print(t)
print(type(t))