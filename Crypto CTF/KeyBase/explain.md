# Keybase
pythonプログラム"keybase.py"が与えられる。
###解析
- AESによる暗号化がCBCモードで行われていることがわかる。CBCモードとはブロック長以上の平文をブロック暗号で暗号化するためのモードの一つで、平文のブロックとその前の暗号文のブロックのXORを暗号化して暗号文のブロックとするものである。最初の平文ブロックはIVと呼ばれる初期値を用い、それは鍵又は暗号文とともに伝達される。
- サーバに接続すると、flagの暗号文または任意の平文の暗号化が行える。flagの暗号文は全て渡される。
- 任意の32バイトの平文を入力すると、一部が隠された暗号文と鍵が渡される。暗号文は中間の14バイト、鍵は最後の2バイトが隠されている。
- 鍵候補は256<sup>2</sup>であり、全探索が可能のように思えるが、以上の二つの操作において、いずれでもIVが渡されないため、実際には18バイト分すなわち256<sup>18</sup>の全探索が要求され、不可能である。


###解法
- AESのブロックは128bitであり、このプログラムでは2ブロック分の操作が行われている。
- 任意の暗号化において、暗号文が隠されているのは前半のブロックであり、後半のブロックは欠損していない。
- 以下の操作を、取り得る鍵候補に対し全探索する。
  1. 暗号文の後半ブロックをECBモードで復号したものは、暗号文の前半ブロックと平文の後半ブロックのXORである。平文の後半ブロックは既知であるため、暗号文の前半ブロックがXORによって求まる。
  2. 前操作によって明らかになった暗号文の前半ブロックを用いて、同様にすることでIVを求める。
  3. 得たIVと鍵でflagの暗号文を復号し、正しい形式であるか確認する。
- この場合全探索の回数は256<sup>2</ssup>であり、十分高速に行える。

###コード
```python
from binascii import unhexlify
from Crypto.Cipher import AES


def bxor(b1, b2):  # use xor for bytes
    parts = []
    for b1, b2 in zip(b1, b2):
        parts.append(bytes([b1 ^ b2]))
    return b''.join(parts)


key_body = "b59a82d047cb72d64b9005651091"
key_body = unhexlify(key_body)
plain = ('a' * 32).encode()
t = unhexlify("8671e5d111c47264b8839a3955bd9623")
encrypted_flag = unhexlify("fdb425f2ecbc7a904fcc190a7e6ed80f3f49069e2740d498c351d4487419e71f")

for _ in range(0, 256 ** 2):
    print(_, ':')
    suffix = _.to_bytes(2, 'big')
    key = key_body + suffix
    aes = AES.new(key, AES.MODE_ECB)
    enc_head = bxor(aes.decrypt(t), plain)
    iv = bxor(aes.decrypt(enc_head), plain)
    DEC = AES.new(key, AES.MODE_CBC, iv)
    flag = DEC.decrypt(encrypted_flag)
    if flag[0:5] == b'CCTF{':
        print(flag.decode('ascii'))
        break
```
