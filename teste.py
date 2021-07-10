from collections import defaultdict

d1 = {3: 2, 1: 4}
d2 = {1: 6, 3: 7}

dd = defaultdict(list)

for d in (d1, d2): # you can list as many input dicts as you want here
    for key, value in d.items():
        dd[key].append(value)

print(dd)