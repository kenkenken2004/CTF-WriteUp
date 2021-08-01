# Farm
Pythonベースの数学処理ソフト「SageMath」のプログラムファイル"farm.sage"が与えられる。

###解析
- 冒頭に"F = list(GF(64))"とあり、Fは位数が64の(64個の元を持つ)有限体であることがわかる。
- 鍵生成関数"keygen(l)"を見ると、ランダムなFの元l個の積を鍵をしていることがわかる。
- 関数"maptofarm(c)"は、文字cを対応するFの元へと変換している。
- 暗号化関数"encrypt(msg,key)"では、以下のことが行われている。<br>
    1. 平文をbase64でエンコードする。
    2. keyを、所定の多項式関数を通してpkeyに変換する。
    3. 平文の文字をFの元へと符号化してpkeyとの積をとり、そ積のFにおける添え字を求める。
    4. 上で求めた添え字の位置にある"ALPHABET"の文字を暗号文とする。
    5. 以上の操作を全ての文字に対して行う。
- コメントアウトに、平文の長さは14であって鍵候補は64<sup>14</sup>個あり、全探索は不可能な旨述べている。

###解法
- 注目すべきは有限体の上で鍵の生成・操作が行われている点である。有限体における四則演算は閉じている。それはすなわちFの元どうしの和・積演算の結果もまたFの元だということである。
- さて、最終的に暗号化に用いられたpkeyは14個のFの元の積の、累乗と和である。この操作は全て和と積に分解される。つまり、pkeyもまたFの元である。
- Fの位数は64であり、それはつまりpkeyが取り得る値も高々それだけしかない。64<sup>14</sup>通りでは決してない。
- これは明らかに全探索がであるため、Fの全ての元に対し、それをpkeyとして復号し、flagらしき平文を見つける。具体的には、
    1. 暗号文の文字を、"ALPHABET.index()"でその添え字を取得する。
    2. "F[]"で、Fにおけるその添え字の位置にある元を取得する。
    3. pkeyで除算する。
    4. その元のFにおける添え字を取得する。
    5. "AKPHABET"におけるその添え字に位置する文字を平文とする。
    6. これを全文字に対し行う。

###コード
```python
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
```