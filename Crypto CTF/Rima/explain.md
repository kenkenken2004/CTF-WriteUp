# Tuti
pythonプログラム"rima.py"、暗号文の"g.enc"、"h.enc"が与えられる。
### 解析
- まず、flagが二進配列fに変換されている。各要素の型は整数である。
- fの先頭に0を挿入し、最後の要素以外にそれぞれ次の要素を足している。
- fの長さの値の次の素数をa、aの次の素数をbとする。
- fをa回繰り返したものをg、b回繰り返したものをhとする。
- fの長さの右シフト２回(約1/4)の次の素数をcとする。
- g,hそれぞれ先頭にc個の0を挿入し、先頭から「g,hの長さ - c」個の要素についてそれぞれc個後の要素の値を足す。
- g,hの各要素をそれぞれ文字列として結合した後5進文字列とみなし整数化し、ファイルにバイナリとして書き込む。

### 解法
- まず最初にflagの文字数を特定する。
    1. 最初の二進配列の長さがnであるとするとき、それに1要素加え、a,b回繰り返しc個足すので以下の式で表せる。
    2. ( n + 1 ) × nextPrime( n + 1 ) + c = gの配列長
    3. ( n + 1 ) × nextPrime( nextPrime( n + 1 ) ) + c = hの配列長
    4. ただし、その後の操作で先頭の0が省略されてしまう可能性があると思うかもしれないが、操作を過程をたどると、先頭は1であることが保証されていることがわかる。
    5. これを全探索すると、n = 255, a = 257, b = 263, c = 67 である事がわかる。
- 後は解析の結果に従って型変換や減算、繰り返し部分の省略など、逆操作を行う。

### コード
```python
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

```
