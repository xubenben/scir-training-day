import time
import random
import numpy

length=10000000
a=[random.random() for i in range(length)]
b=[random.random() for i in range(length)]
c=[]
start=time.time()
for index in range(1000):
    c=[]
    for i,j in zip(a,b):
         c.append(i*j)
    end=time.time()
print "list: " 
print end-start

a=numpy.random.random_sample(length)
b=numpy.random.random_sample(length)
start=time.time()
for index in range(1000):
    d=a*b
end=time.time()
print "numpy: "
print end-start

