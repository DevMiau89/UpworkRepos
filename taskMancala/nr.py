import matplotlib.pyplot as plt

N = 17
d = 3
# 1 + 2 + 2*2 + 2**3 = 14+1

# (b**(d+1) - 1) / (b - 1) ~ b**(d+1) / b = b**d
# b**d ~ N+1
# b ~ (N+1)**(1./d)

def g(b):
    mysum = 1
    for i in range(1, d+1):
        mysum += b**i
    return mysum - (N+1)
    
def dg(b):
    mysum = 1
    for i in range(1, d):
        mysum += (i+1)*b**i
    return mysum

def newton(b0, g, dg):
    b = [b0]
    for n in range(0, 10):
        print(b[n])
        b.append( b[n] - g(b[n])/ dg(b[n]) )
    return b

b0 = (N+1)**(1./d)
b = newton(b0, g, dg)

print("Check:")
print( g(b[-1]) )

plt.plot(range(len(b)), map(g, b))
plt.show()
