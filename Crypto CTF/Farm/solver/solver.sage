import string, base64, math

ALPHABET = string.printable[:62] + '\\='

F = list(GF(64))

def decrypt(enc):
	for key in F[1:]:
		dec = b""
		for _ in enc:
			dec += ord(ALPHABET[F.index(F[ALPHABET.index(_)] / key)]).to_bytes(1,'big')
		try:
			dec = base64.b64decode(dec)
			try:
				print(dec.decode())
			except:
				print("fail")
		except:
				print("fail")



decrypt("805c9GMYuD5RefTmabUNfS9N9YrkwbAbdZE0df91uCEytcoy9FDSbZ8Ay8jj")

