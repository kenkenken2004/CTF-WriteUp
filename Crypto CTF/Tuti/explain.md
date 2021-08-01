# Tuti
pythonプログラム"tuti.py"が与えられる。
###解析
- 最初にflagを前後に分割し、それぞれを整数のバイト列とみなして整数化していて、前半をx、後半をyとしている。
- 整数kが16進数文字列で記述されている。
- assert文から、以下の式が満たされることがわかる。
- ( x<sup>2</sup> + 1 )( y<sup>2</sup> + 1 ) - 2( x - y )( xy - 1 ) = 4( k + xy )

###解法
- x,yの項を因数分解すると、以下の式になる。
- ( x + 1 )<sup>2</sup>( y - 1 )<sup>2</sup> = 4k
- つまり、kの4倍の平方根の約数の中にx+1とy-1があるということである。
- 素因数分解ソフトmsieve153を用いて素因数分解する。
- 求めた素因数に対してbit全探索を行い、約数を列挙しx,yを出す。
- x,yをバイト列として連結し、正しいflag文字列かどうか判断する。
- 素因数は高々10数個であるので十分に高速である。

###コード
```python
def root(b, r):
    x = 1
    v = 0
    do = True
    while do:
        if (v + x) ** r == b:
            return v + x
        elif (v + x) ** r < b:
            v += x
            x *= 2
        else:
            x = x // 2
        if x == 0:
            do = False
    return -1


k = '''
000bfdc32162934ad6a054b4b3db8578674e27a165113f8ed018cbe9112
4fbd63144ab6923d107eee2bc0712fcbdb50d96fdf04dd1ba1b69cb1efe
71af7ca08ddc7cc2d3dfb9080ae56861d952e8d5ec0ba0d3dfdf2d12764
'''.replace('\n', '')
k = int(k, 16)
k = root(4 * k, 2)
print("k:",k)

# msieve153で素因数を求める。

factors = [2, 2, 3, 11, 11, 19, 47, 71, 3449, 11953, 5485619, 2035395403834744453, 17258104558019725087,
           1357459302115148222329561139218955500171643099]
n = len(factors)
for i in range(2 ** n):
    m_1 = 1
    for j in range(n):
        if (i >> j) & 1:
            m_1 *= factors[j]
    if hex(m_1 - 1)[:12] == "0x434354467b":
        m_2 = k // m_1 + 1
        m_1 -= 1
        head = m_1.to_bytes(22,'big').decode()
        suf = m_2.to_bytes(22,'big').decode()
        flag = head + suf
        print(flag)
        break
```
