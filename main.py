
import glob
import importlib

test_modules = []
for filename in sorted(glob.glob('test??_*.py')):
    m = importlib.import_module(filename.replace(".py", ""))
    test_modules.append(m)

# print(test_modules)


length = 400000

import random
bits = "{0:b}".format(random.getrandbits(length))
bits = [ int(c) for c in bits ]

print("==========================")
print("random")
print("==========================")
for i, test_module in enumerate(test_modules):
    P_value, level, ok = test_module.test(bits)
    print(test_module.__name__, end="\t")
    print(P_value, end="\t")
    print(ok)


import secrets
bits = "{0:b}".format(secrets.randbits(length))
bits = [ int(c) for c in bits ]

print("==========================")
print("secrets")
print("==========================")
for i, test_module in enumerate(test_modules):
    P_value, level, ok = test_module.test(bits)
    print(test_module.__name__, end="\t")
    print(P_value, end="\t")
    print(ok)
