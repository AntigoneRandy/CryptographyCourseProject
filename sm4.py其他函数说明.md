# sm4.py其他函数说明

## 1.加密函数

clear_num是一组明文，首先调用byte2Tuple函数，将明文存成元组，再转换成列表。然后调用makeRoundKey函数，把mk（密钥）传进去，获取32个轮密钥。之后进行32轮加密，每次使用一个轮密钥。最后将结果反序，元组变回字节形式返回。

```python
def encrypt(clear_num, mk):
    x_keys = list(byte2Tuple(clear_num, byte_n=16))
    round_keys = makeRoundKey(mk)
    for i in range(32):
        x_keys.append(roundF(x_keys[i:i + 4], round_keys[i]))
    return tuple2Byte(x_keys[-4:][::-1], byte_n=16)
```

## 2.解密函数

只和加密函数有一处区别：轮密钥顺序颠倒。

```python
def decrypt(cipher_num, mk):
    x_keys = list(byte2Tuple(cipher_num, byte_n=16))
    round_keys = makeRoundKey(mk)
    # 区别就在下面这一行
    round_keys = round_keys[::-1]
    for i in range(32):
        x_keys.append(roundF(x_keys[i:i + 4], round_keys[i]))
    return tuple2Byte(x_keys[-4:][::-1], byte_n=16)
```

## 3.填充（这里暂时留给师腾）

## 4.字符转十六进制

判断一下参数是字符串还是字节形式。如果是字符串，就用UTF8编码转换一下，否则直接赋值给byte。调用hexlify函数把它转成十六进制，用于后续的处理。

```python
def _hex(str_or_bytes):
    if isinstance(str_or_bytes, str):
        byte = str_or_bytes.encode(encoding='UTF8')
    elif isinstance(str_or_bytes, bytes):
        byte = str_or_bytes
    else:
        byte = b''
    hex_str = hexlify(byte)
    return hex_str
```

## 5.ECB加密&解密

首先如果明文分组后的最后一组的长度不够，就填充一下。加一个判断语句，如果没有获取到明文，就直接终止程序。

接下来，把明文转换成十六进制。len(plain_text) // BLOCK_BYTE表示明文的组数，对于每组明文，取它的十六进制形式，调用encrypt函数进行加密。由于encrypt返回值是int型，因此需要调用num2hex来把int型转换成十六进制数，存到密文十六进制缓存里。最后把密文从十六进制变成字符格式即可。

```python
def encrypt_ecb(plain_text, key):
    start = time.perf_counter()
    plain_text = _padding(plain_text, mode=SM4_ENCRYPT)
    if plain_text is None:
        return

    plain_hex = _hex(plain_text)
    cipher_hex_list = []
    for i in range(len(plain_text) // BLOCK_BYTE):
        sub_hex = plain_hex[i * BLOCK_HEX:(i + 1) * BLOCK_HEX]
        cipher = encrypt(clear_num=int(sub_hex, 16),
                         mk=int(_hex(key), 16))
        cipher_hex_list.append(num2hex(num=cipher, width=BLOCK_HEX))

    cipher_text = b64encode(_unhex(''.join(cipher_hex_list)))
    end = time.perf_counter()

    return cipher_text, (end - start)*1000
```

解密基本一样，就是个逆过程，明文换成密文就行了，然后类型转换的顺序颠倒一下。这里不用管轮密钥的顺序，因为前面的decrypt已经做好了。

## 6.CBC加密&解密

总体结构和普通加解密差不多，重点在一个初始向量iv上。在加密时，它会与第一组明文先作一个异或运算，然后再送入加密函数。加密后产生密文，将这个密文与下一组明文作异或后再加密。如此，除第一组外，每一组明文在加密前都要与上一组密文作异或运算。

解密时，可想而知，密文直接送入解密函数，解密出来的结果是对应明文与上一组密文异或后的结果，因此需要对解密出来的结果再做一次异或，就可以得到明文了。当然，第一组需要跟初始向量iv异或。

大致原理如下

![img](https://myh-mdpictures.oss-cn-qingdao.aliyuncs.com/img/aHR0cHM6Ly90dmExLnNpbmFpbWcuY24vbGFyZ2UvMDA2dE5iUndseTFnYXlyZGQyZnhnajMwankwZ3A3NmQuanBn)

与ECB对比如下

![img](https://myh-mdpictures.oss-cn-qingdao.aliyuncs.com/img/20180901170901225)

```python
def encrypt_cbc(plain_text, key, iv):
    start = time.perf_counter()
    plain_text = _padding(plain_text, mode=SM4_ENCRYPT)
    if plain_text is None:
        return

    plain_hex = _hex(plain_text)
    ivs = [int(_hex(iv), 16)]
    for i in range(len(plain_text) // BLOCK_BYTE):
        sub_hex = plain_hex[i * BLOCK_HEX:(i + 1) * BLOCK_HEX]
        cipher = encrypt(clear_num=(int(sub_hex, 16) ^ ivs[i]),
                         mk=int(_hex(key), 16))
        ivs.append(cipher)

    cipher_text = b64encode(_unhex(''.join([num2hex(num=c, width=BLOCK_HEX)
                                            for c in ivs[1:]])))
    end = time.perf_counter()
    return cipher_text, (end - start) * 1000
```

代码的流程就是这样。把传入的iv处理成十六进制后，在加密前与该组明文作异或，并且每一组加密后，产生的密文送到iv的末尾，下次取用时iv就是上一组的密文了。