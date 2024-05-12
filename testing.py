from dict import *
s=int('4c',16)
res=str(bin(s)[2:])
print(res)
source=res[-3::1]
des=res[-6:-3:1]
print(source,des)
print("source:",register[source],"des:",register[des])
s="hello word"
print(s[-3::1])