# Cipher_stealth密文挪用模式代码说明







## 关于padding 与 stealth 
padding（） 是一种比较简单的用于断块处理的函数 ，给明文填入特定字符到整数个块的长度
    
stealth 指 cipher stealth 密文挪用模式 。针对不同的工作模式（ecb，cbc）实现方式不同，用于短块填充，与之对应的是classic ，classic模式使用padding进行短块填充

### Classic 模式：padding 与 unpadding

```python
     # unicode
    if isinstance(text, text_type):
        text = text.encode(encoding=E_FMT)

    if mode == SM4_ENCRYPT:
        # 填充
        p_num = BLOCK_BYTE - (len(text) % BLOCK_BYTE)
        space = '' if PY2 else b''
        pad_s = (chr(p_num) * p_num) if PY2 else (chr(p_num).encode(E_FMT) * p_num)
        res = space.join([text, pad_s])
    else:
        # 去填充
        p_num = ord(text[-1]) if PY2 else text[-1]
        res = text[:-p_num]
    return res
```
填充byte串
填充和去填充由mode决定，p_num表示填充字节数 ，pad_s为填充内容 ，即pnum个chr（pnum）

填充之后按顺序加密各个块，解密时读取最后一个块最后一字节即可获得填充内容和填充长度，去掉即可

### stealth 模式 密文挪用：

#### ecb_stealth
初始明文不进行填充，直接加密到n-1块，
```python
    plain_hex = _hex(plain_text)
    cipher_hex_list = []
    for i in _range(len(plain_text) // BLOCK_BYTE):
        sub_hex = plain_hex[i * BLOCK_HEX:(i + 1) * BLOCK_HEX]
        cipher = encrypt(clear_num=int(sub_hex, 16),
                         mk=int(_hex(key), 16))
        cipher_hex_list.append(num2hex(num=cipher, width=BLOCK_HEX))
```
取出短块（最后一块）明文与第n-1块密文拼接，
```python
        sub_hex = plain_hex[ len(plain_text) // BLOCK_BYTE * BLOCK_HEX : ] #get short block
        short_length = len(sub_hex)
        cipher_n_1 = bytes(cipher_hex_list[len(plain_text) // BLOCK_BYTE - 1],encoding="utf-8") # get block n-1
        
        sub_hex=sub_hex + cipher_n_1[ -( 32 - len(sub_hex)) : ] #padding short block
```
补齐短块，将n-1块密文（剩余部分）放回，
```python
        cipher_n_1_new = cipher_hex_list[len(plain_text) // BLOCK_BYTE - 1][0: short_length] # refresh block n-1
    
        cipher_hex_list[len(plain_text) // BLOCK_BYTE - 1] = cipher_n_1_new #put n-1 back
```
加密短块，最后将短块密文放到密文末尾

```python
        cipher = encrypt(clear_num=int(sub_hex, 16),
                         mk=int(_hex(key), 16))
        

        cipher_hex_list.append(num2hex(num=cipher, width=BLOCK_HEX))
```

保证了明文和密文长度（十六进制位数）相同

#### cbc_stealth
初始明文不填充，加密到n-1块，
```python
    #generate cipher of 1 ~ n-1 block 
    for i in _range(len(plain_text) // BLOCK_BYTE):
        sub_hex = plain_hex[i * BLOCK_HEX:(i + 1) * BLOCK_HEX]
        cipher = encrypt(clear_num=(int(sub_hex, 16) ^ ivs[i]),
                         mk=int(_hex(key), 16))
        ivs.append(cipher)
```
将n-1块密文与短块直接异或补齐短块（由于异或操作数是int，因此用指数乘来移位）
```python
    #generate cipher(int) of last block
    if len(plain_text) %BLOCK_BYTE != 0 :

        if len(plain_text) < BLOCK_BYTE :
            print('Length of plain text lower than 16,can not use stealth mod')
            return 
        
        sub_hex = plain_hex[len(plain_text) // BLOCK_BYTE * BLOCK_HEX : ]
        
        short_length = len(sub_hex)
        #cipher stealth
        
        cipher = encrypt(clear_num=((int(sub_hex, 16) * pow(16,32-short_length)) ^ ivs[-1]),
                         mk=int(_hex(key), 16))
        #cipher = encrypt(short_block XOR block n-1)
        ivs.append(cipher)
```
计算短块密文，将第n-1块密文截取到短块长，
产生密文
```python
    #refresh cipher block n-1
    cipher_temp[-2] = cipher_temp[-2][0 : short_length]

    #generate cipher text
    cipher_text = ''
    for c in cipher_temp:
        cipher_text += c
```
