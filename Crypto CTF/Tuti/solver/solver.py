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
