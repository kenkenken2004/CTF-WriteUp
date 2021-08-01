from Crypto.Util.number import *
from numpy import base_repr


def analyze(g_len, h_len):
    n = 0
    while True:
        n += 1
        a = nextPrime(n)
        b = nextPrime(a)
        c = nextPrime(n >> 2)
        if n*a + c == g_len and n*b + c == h_len:
            break
    return n - 1, a, b, c


def nextPrime(n):
    while True:
        n += (n % 2) + 1
        if isPrime(n):
            return n


file_g = open('g.enc', 'rb')
file_h = open('h.enc', 'rb')
g = [int(_) for _ in format(base_repr(bytes_to_long(file_g.read()), 5))]
h = [int(_) for _ in format(base_repr(bytes_to_long(file_h.read()), 5))]

n, a, b, c = analyze(len(g), len(h))

for i in range(len(g) - c).__reversed__():
    g[i] -= g[i + c]
g = g[67:323]

for i in range(len(g) - 1).__reversed__():
    g[i] -= g[i + 1]
g = g[1:]
g.reverse()
n = 1
t = 0
for _ in g:
    t += n * _
    n *= 2
t = long_to_bytes(t)
print(t.decode())
