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
