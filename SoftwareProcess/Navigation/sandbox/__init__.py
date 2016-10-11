l = []

l1 = ["A", "2016-10-11", "12:24:05"]
l2 = ["B", "2016-10-11", "12:24:05"]
l3 = ["C", "2016-10-11", "08:24:05"]
l4 = ["D", "2016-09-11", "12:24:05"]

l.append(l1)
l.append(l2)
l.append(l3)
l.append(l4)

print "Before sort: \n"

for line in l:
    print line
    
l.sort(key=lambda x: (x[1], x[2], x[0]))
    
print "After sort: \n"

for line in l:
    print line
    
    