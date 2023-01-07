#!/usr/bin/env python
# -*- coding: utf-8 -*-


# from sys import version_info

from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify
import time

# __all__ = ['encrypt_ecb', 'decrypt_ecb',
#            'encrypt_cbc', 'decrypt_cbc']

# if version_info[0] == 2:
#     # python2
#     PY2 = True
#     PY3 = False
# else:
#     # python3
#     PY2 = False
#     PY3 = True

# if PY2:
#     range = xrange
#     string_types = (basestring,)
#     str = unicode
#     bytes = str
# else:
#     range = range
#     string_types = (str,)
#     str = str
#     bytes = bytes

# string_types = (str,)
# 'UTF8' = 'UTF8'

# S盒
S_BOX = {
    0x00: 0xD6, 0x01: 0x90, 0x02: 0xE9, 0x03: 0xFE, 0x04: 0xCC, 0x05: 0xE1, 0x06: 0x3D, 0x07: 0xB7,
    0x08: 0x16, 0x09: 0xB6, 0x0A: 0x14, 0x0B: 0xC2, 0x0C: 0x28, 0x0D: 0xFB, 0x0E: 0x2C, 0x0F: 0x05,
    0x10: 0x2B, 0x11: 0x67, 0x12: 0x9A, 0x13: 0x76, 0x14: 0x2A, 0x15: 0xBE, 0x16: 0x04, 0x17: 0xC3,
    0x18: 0xAA, 0x19: 0x44, 0x1A: 0x13, 0x1B: 0x26, 0x1C: 0x49, 0x1D: 0x86, 0x1E: 0x06, 0x1F: 0x99,
    0x20: 0x9C, 0x21: 0x42, 0x22: 0x50, 0x23: 0xF4, 0x24: 0x91, 0x25: 0xEF, 0x26: 0x98, 0x27: 0x7A,
    0x28: 0x33, 0x29: 0x54, 0x2A: 0x0B, 0x2B: 0x43, 0x2C: 0xED, 0x2D: 0xCF, 0x2E: 0xAC, 0x2F: 0x62,
    0x30: 0xE4, 0x31: 0xB3, 0x32: 0x1C, 0x33: 0xA9, 0x34: 0xC9, 0x35: 0x08, 0x36: 0xE8, 0x37: 0x95,
    0x38: 0x80, 0x39: 0xDF, 0x3A: 0x94, 0x3B: 0xFA, 0x3C: 0x75, 0x3D: 0x8F, 0x3E: 0x3F, 0x3F: 0xA6,
    0x40: 0x47, 0x41: 0x07, 0x42: 0xA7, 0x43: 0xFC, 0x44: 0xF3, 0x45: 0x73, 0x46: 0x17, 0x47: 0xBA,
    0x48: 0x83, 0x49: 0x59, 0x4A: 0x3C, 0x4B: 0x19, 0x4C: 0xE6, 0x4D: 0x85, 0x4E: 0x4F, 0x4F: 0xA8,
    0x50: 0x68, 0x51: 0x6B, 0x52: 0x81, 0x53: 0xB2, 0x54: 0x71, 0x55: 0x64, 0x56: 0xDA, 0x57: 0x8B,
    0x58: 0xF8, 0x59: 0xEB, 0x5A: 0x0F, 0x5B: 0x4B, 0x5C: 0x70, 0x5D: 0x56, 0x5E: 0x9D, 0x5F: 0x35,
    0x60: 0x1E, 0x61: 0x24, 0x62: 0x0E, 0x63: 0x5E, 0x64: 0x63, 0x65: 0x58, 0x66: 0xD1, 0x67: 0xA2,
    0x68: 0x25, 0x69: 0x22, 0x6A: 0x7C, 0x6B: 0x3B, 0x6C: 0x01, 0x6D: 0x21, 0x6E: 0x78, 0x6F: 0x87,
    0x70: 0xD4, 0x71: 0x00, 0x72: 0x46, 0x73: 0x57, 0x74: 0x9F, 0x75: 0xD3, 0x76: 0x27, 0x77: 0x52,
    0x78: 0x4C, 0x79: 0x36, 0x7A: 0x02, 0x7B: 0xE7, 0x7C: 0xA0, 0x7D: 0xC4, 0x7E: 0xC8, 0x7F: 0x9E,
    0x80: 0xEA, 0x81: 0xBF, 0x82: 0x8A, 0x83: 0xD2, 0x84: 0x40, 0x85: 0xC7, 0x86: 0x38, 0x87: 0xB5,
    0x88: 0xA3, 0x89: 0xF7, 0x8A: 0xF2, 0x8B: 0xCE, 0x8C: 0xF9, 0x8D: 0x61, 0x8E: 0x15, 0x8F: 0xA1,
    0x90: 0xE0, 0x91: 0xAE, 0x92: 0x5D, 0x93: 0xA4, 0x94: 0x9B, 0x95: 0x34, 0x96: 0x1A, 0x97: 0x55,
    0x98: 0xAD, 0x99: 0x93, 0x9A: 0x32, 0x9B: 0x30, 0x9C: 0xF5, 0x9D: 0x8C, 0x9E: 0xB1, 0x9F: 0xE3,
    0xA0: 0x1D, 0xA1: 0xF6, 0xA2: 0xE2, 0xA3: 0x2E, 0xA4: 0x82, 0xA5: 0x66, 0xA6: 0xCA, 0xA7: 0x60,
    0xA8: 0xC0, 0xA9: 0x29, 0xAA: 0x23, 0xAB: 0xAB, 0xAC: 0x0D, 0xAD: 0x53, 0xAE: 0x4E, 0xAF: 0x6F,
    0xB0: 0xD5, 0xB1: 0xDB, 0xB2: 0x37, 0xB3: 0x45, 0xB4: 0xDE, 0xB5: 0xFD, 0xB6: 0x8E, 0xB7: 0x2F,
    0xB8: 0x03, 0xB9: 0xFF, 0xBA: 0x6A, 0xBB: 0x72, 0xBC: 0x6D, 0xBD: 0x6C, 0xBE: 0x5B, 0xBF: 0x51,
    0xC0: 0x8D, 0xC1: 0x1B, 0xC2: 0xAF, 0xC3: 0x92, 0xC4: 0xBB, 0xC5: 0xDD, 0xC6: 0xBC, 0xC7: 0x7F,
    0xC8: 0x11, 0xC9: 0xD9, 0xCA: 0x5C, 0xCB: 0x41, 0xCC: 0x1F, 0xCD: 0x10, 0xCE: 0x5A, 0xCF: 0xD8,
    0xD0: 0x0A, 0xD1: 0xC1, 0xD2: 0x31, 0xD3: 0x88, 0xD4: 0xA5, 0xD5: 0xCD, 0xD6: 0x7B, 0xD7: 0xBD,
    0xD8: 0x2D, 0xD9: 0x74, 0xDA: 0xD0, 0xDB: 0x12, 0xDC: 0xB8, 0xDD: 0xE5, 0xDE: 0xB4, 0xDF: 0xB0,
    0xE0: 0x89, 0xE1: 0x69, 0xE2: 0x97, 0xE3: 0x4A, 0xE4: 0x0C, 0xE5: 0x96, 0xE6: 0x77, 0xE7: 0x7E,
    0xE8: 0x65, 0xE9: 0xB9, 0xEA: 0xF1, 0xEB: 0x09, 0xEC: 0xC5, 0xED: 0x6E, 0xEE: 0xC6, 0xEF: 0x84,
    0xF0: 0x18, 0xF1: 0xF0, 0xF2: 0x7D, 0xF3: 0xEC, 0xF4: 0x3A, 0xF5: 0xDC, 0xF6: 0x4D, 0xF7: 0x20,
    0xF8: 0x79, 0xF9: 0xEE, 0xFA: 0x5F, 0xFB: 0x3E, 0xFC: 0xD7, 0xFD: 0xCB, 0xFE: 0x39, 0xFF: 0x48
}

# 系统参数FK
FK = (0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC)

# 固定参数CK
CK = (0x00070E15, 0x1C232A31, 0x383F464D, 0x545B6269, 0x70777E85, 0x8C939AA1, 0xA8AFB6BD, 0xC4CBD2D9,
      0xE0E7EEF5, 0xFC030A11, 0x181F262D, 0x343B4249, 0x50575E65, 0x6C737A81, 0x888F969D, 0xA4ABB2B9,
      0xC0C7CED5, 0xDCE3EAF1, 0xF8FF060D, 0x141B2229, 0x30373E45, 0x4C535A61, 0x686F767D, 0x848B9299,
      0xA0A7AEB5, 0xBCC3CAD1, 0xD8DFE6ED, 0xF4FB0209, 0x10171E25, 0x2C333A41, 0x484F565D, 0x646B7279)

# 轮密钥缓存
roundkey_tmp = {}

# 加密
SM4_ENCRYPT = 1
# 解密
SM4_DECRYPT = 0
# 分组byte数
BLOCK_BYTE = 16
BLOCK_HEX = BLOCK_BYTE * 2


def num2hex(num, width=1):
    """
    整数转为指定长度的十六进制字符串，不足补0
    >>> num2hex(1000, width=4)
    '03e8'
    :param num: 整数
    :param width: 16进制字符串长度， 默认为1
    :return str
    """
    return '{:0>{width}}'.format(hex(num)[2:].replace('L', ''),
                                 width=width)


def byte2Tuple(num, byte_n=4):
    # 分解后元组长度
    tuple_len = 4
    # 步长
    step = (byte_n // tuple_len) * 2
    hex_str = num2hex(num=num, width=byte_n * 2)
    split_v = list(range(len(hex_str)))[::step] + [len(hex_str)]
    return tuple([int(hex_str[i:j], base=16) for i, j in
                  zip(split_v[:-1], split_v[1:])])


def tuple2Byte(byte_array, byte_n=4):
    tuple_len = 4
    # byte_array每一项16进制字符串的长度
    width = (byte_n // tuple_len) * 2
    if len(byte_array) != tuple_len:
        raise ValueError('byte_array length must be 4.')
    return int(''.join([num2hex(num=i, width=width)
                        for i in byte_array]), 16)


def sBoxMapping(byte):
    return S_BOX.get(byte)


def notLinearMappingTau(byte_array):
    """
    非线性变换, 输入A=(a0, a1, a2, a3)
    (b0, b1, b2, b3) = (Sbox(a0), Sbox(a1), Sbox(a2), Sbox(a3))
    """
    return (sBoxMapping(byte_array[0]), sBoxMapping(byte_array[1]),
            sBoxMapping(byte_array[2]), sBoxMapping(byte_array[3]))


def linearMappingForEncrypt(byte4):
    """
    线性变换L
    L(B) = B ⊕ (B <<< 2) ⊕ (B <<< 10) ⊕ (B <<< 18) ⊕ (B <<< 24)
    """
    # _left = loopLeft
    return byte4 ^ loopLeft(byte4, 2) ^ loopLeft(byte4, 10) ^ loopLeft(byte4, 18) ^ loopLeft(byte4, 24)


def linearMappingForRoundKey(byte4):
    """
    线性变换L'
    L'(B) = B ⊕ (B <<< 13) ⊕ (B <<< 23)
    """
    # _left = loopLeft
    return byte4 ^ loopLeft(byte4, 13) ^ loopLeft(byte4, 23)


def loopLeft(num, offset, base=32):
    """
    循环向左移位
    >>> loopLeft(0b11010000, 3, base=8)
    >>> 0b10000110
    """
    bin_str = '{:0>{width}}'.format(bin(num)[2:], width=base)
    rem = offset % base
    return int(bin_str[rem:] + bin_str[:rem], 2)


def TForEncrypt(byte4):
    """合成置换T, 由非线性变换和线性变换L复合而成"""
    # 非线性变换
    b_array = notLinearMappingTau(byte2Tuple(byte4))
    # 线性变换L
    return linearMappingForEncrypt(tuple2Byte(b_array))


def TForRoundKey(byte4):
    """
    合成置换T', 由非线性变换和线性变换L'复合而成
    """
    # 非线性变换
    b_array = notLinearMappingTau(byte2Tuple(byte4))
    # 线性变换L'
    return linearMappingForRoundKey(tuple2Byte(b_array))


def makeRoundKey(mk):
    """
    轮密钥由加密密钥通过密钥扩展算法生成
    加密密钥MK = (MK0, MK1, MK2, MK3)
    轮密钥生成算法:
    (K0, K1, K2, K3) = (MK0 ⊕ FK0, MK1 ⊕ FK1, MK2 ⊕ FK2, MK3 ⊕ FK3)
    rki = Ki+4 = Ki⊕T'(Ki+1 ⊕ Ki+2 ⊕ Ki+3 ⊕ CKi) i=0, 1,...,31
    :param mk: 加密密钥, 16byte, 128bit
    :return list
    """
    # 尝试从轮密钥缓存中获取轮密钥
    # 没有获取到, 根据密钥扩展算法生成
    roundkeys = roundkey_tmp.get(mk)
    if roundkeys is None:
        mk0, mk1, mk2, mk3 = byte2Tuple(mk, byte_n=16)
        keys = [mk0 ^ FK[0], mk1 ^ FK[1], mk2 ^ FK[2], mk3 ^ FK[3]]
        for i in range(32):
            rk = keys[i] ^ TForRoundKey(
                keys[i + 1] ^ keys[i + 2] ^ keys[i + 3] ^ CK[i])
            keys.append(rk)
        roundkeys = keys[4:]
        # 加入轮密钥缓存中
        roundkey_tmp[mk] = roundkeys
    return roundkeys


def roundF(byte4_array, rk):
    """
    轮函数, F(X0, X1, X2, X3, rk) = X0 ⊕ T(X1 ⊕ X2 ⊕ X3 ⊕ rk)
    :param byte4_array: (X0, X1, X2, X3), 每一项4byte, 32bit
    :param rk: 轮密钥, 4byte, 32bit
    """
    x0, x1, x2, x3 = byte4_array
    return x0 ^ TForEncrypt(x1 ^ x2 ^ x3 ^ rk)


# def _crypt(num, mk, mode=SM4_ENCRYPT):
#     """
#     SM4加密和解密
#     :param num: 密文或明文 16byte
#     :param mk:  密钥 16byte
#     :param mode: 轮密钥顺序
#     """
#     x_keys = list(byte2Tuple(num, byte_n=16))
#     round_keys = makeRoundKey(mk)
#     if mode == SM4_DECRYPT:
#         round_keys = round_keys[::-1]
#     for i in range(32):
#         x_keys.append(roundF(x_keys[i:i + 4], round_keys[i]))
#     return tuple2Byte(x_keys[-4:][::-1], byte_n=16)


def encrypt(clear_num, mk):
    """
    SM4加密算法由32次迭代运算和1次反序变换R组成.
    明文输入为(X0, X1, X2, X3), 每一项4byte, 密文输出为(Y0, Y1, Y2, Y3), 每一项4byte
    轮密钥为rki, i=0,1,...,32, 4byte, 运算过程如下:
    1). 32次迭代运算: Xi+4 = F(Xi, Xi+1, Xi+2, Xi+3, rki), i=0,1,...,32
    2). 反序变换: (Y0, Y1, Y2, Y3) = (X35, X34, X33, X32)
    :param clear_num: 明文, 16byte
    :param mk: 密钥, 16byte
    """
    x_keys = list(byte2Tuple(clear_num, byte_n=16))
    round_keys = makeRoundKey(mk)
    for i in range(32):
        x_keys.append(roundF(x_keys[i:i + 4], round_keys[i]))
    return tuple2Byte(x_keys[-4:][::-1], byte_n=16)
    # return _crypt(num=clear_num, mk=mk)


def decrypt(cipher_num, mk):
    """
    SM4解密算法, 解密变换与加密变换结构相同, 不同的仅是轮密钥的使用顺序.
    解密时轮密钥使用顺序为(rk31,rk30,...,rk0)
    :param cipher_num: 密文, 16byte
    :param mk: 密钥, 16byte
    """
    x_keys = list(byte2Tuple(cipher_num, byte_n=16))
    round_keys = makeRoundKey(mk)
    round_keys = round_keys[::-1]
    for i in range(32):
        x_keys.append(roundF(x_keys[i:i + 4], round_keys[i]))
    return tuple2Byte(x_keys[-4:][::-1], byte_n=16)
    # return _crypt(num=cipher_num, mk=mk, mode=SM4_DECRYPT)


def _padding(text, mode=SM4_ENCRYPT):
    """
    加密填充和解密去填充
    """
    # python2 is (basestring, )
    # python3 is (str, bytes)
    # _str_or_bytes = string_types if PY2 else (string_types + (bytes,))
    _str_or_bytes = ((str,) + (bytes,))
    if text is None or not isinstance(text, _str_or_bytes):
        return

    # unicode
    if isinstance(text, str):
        text = text.encode(encoding='UTF8')

    if mode == SM4_ENCRYPT:
        # 填充
        p_num = BLOCK_BYTE - (len(text) % BLOCK_BYTE)
        # space = '' if PY2 else b''
        # pad_s = (chr(p_num) * p_num) if PY2 else (chr(p_num).encode('UTF8') * p_num)
        space = b''
        pad_s = (chr(p_num).encode('UTF8') * p_num)
        res = space.join([text, pad_s])
    else:
        # 去填充
        # p_num = ord(text[-1]) if PY2 else text[-1]
        p_num = text[-1]
        res = text[:-p_num]
    return res


# def _key_iv_check(key_iv):
#     """
#     密钥或初始化向量检测
#     """
#     # 密钥
#     if key_iv is None or not isinstance(key_iv, string_types):
#         raise TypeError(
#             'Parameter key or iv:{} not a basestring'.format(key_iv))

#     if isinstance(key_iv, str):
#         key_iv = key_iv.encode(encoding='UTF8')

#     if len(key_iv) > BLOCK_BYTE:
#         raise ValueError('Parameter key or iv:{} byte greater than {}'.format(key_iv.decode('UTF8'),
#                                                                               BLOCK_BYTE))
#     return key_iv


def _hex(str_or_bytes):
    # PY2: _hex('北京') --> 'e58c97e4baac'
    # PY3: _hex('北京') --> b'e58c97e4baac'
    # if PY2:
    #     hex_str = hexlify(str_or_bytes)
    # else:
    #     # python3
    #     if isinstance(str_or_bytes, str):
    #         byte = str_or_bytes.encode(encoding='UTF8')
    #     elif isinstance(str_or_bytes, bytes):
    #         byte = str_or_bytes
    #     else:
    #         byte = b''
    #     hex_str = hexlify(byte)
    if isinstance(str_or_bytes, str):
        byte = str_or_bytes.encode(encoding='UTF8')
    elif isinstance(str_or_bytes, bytes):
        byte = str_or_bytes
    else:
        byte = b''
    hex_str = hexlify(byte)
    return hex_str


def _unhex(hex_str):
    # PY2: _unhex('e58c97e4baac') --> '\xe5\x8c\x97\xe4\xba\xac'
    # PY3: _unhex('e58c97e4baac') --> b'\xe5\x8c\x97\xe4\xba\xac'
    return unhexlify(hex_str)

# 电子密码本(ECB)


def encrypt_ecb(plain_text, key):
    """
    SM4(ECB)加密
    :param plain_text: 明文
    :param key: 密钥, 小于等于16字节
    """
    start = time.perf_counter()
    plain_text = _padding(plain_text, mode=SM4_ENCRYPT)
    if plain_text is None:
        return

    # 密钥检验
    # key = _key_iv_check(key_iv=key)

    plain_hex = _hex(plain_text)
    cipher_hex_list = []
    for i in range(len(plain_text) // BLOCK_BYTE):
        sub_hex = plain_hex[i * BLOCK_HEX:(i + 1) * BLOCK_HEX]
        cipher = encrypt(clear_num=int(sub_hex, 16),
                         mk=int(_hex(key), 16))
        cipher_hex_list.append(num2hex(num=cipher, width=BLOCK_HEX))

    cipher_text = b64encode(_unhex(''.join(cipher_hex_list)))
    end = time.perf_counter()
    # .decode('UTF8')
    # return cipher_text if PY2 else cipher_text, (end - start)*1000
    return cipher_text, (end - start)*1000


def decrypt_ecb(cipher_text, key):
    """
    SM4(ECB)解密
    :param cipher_text: 密文
    :param key: 密钥, 小于等于16字节
    """
    start = time.perf_counter()
    cipher_text = b64decode(cipher_text)
    cipher_hex = _hex(cipher_text)

    # 密码检验
    # key = _key_iv_check(key_iv=key)
    plain_hex_list = []
    for i in range(len(cipher_text) // BLOCK_BYTE):
        sub_hex = cipher_hex[i * BLOCK_HEX:(i + 1) * BLOCK_HEX]
        plain = decrypt(cipher_num=int(sub_hex, 16),
                        mk=int(_hex(key), 16))
        plain_hex_list.append(num2hex(num=plain, width=BLOCK_HEX))

    plain_text = _padding(_unhex(''.join(plain_hex_list)),
                          mode=SM4_DECRYPT)
    end = time.perf_counter()
    # return plain_text if PY2 else plain_text, (end - start)*1000
    return plain_text, (end - start)*1000
    # .decode('UTF8')


# 密码块链接(CBC)
def encrypt_cbc(plain_text, key, iv):
    """
    SM4(CBC)加密
    :param plain_text: 明文
    :param key: 密钥, 小于等于16字节
    :param iv: 初始化向量, 小于等于16字节
    """
    start = time.perf_counter()
    plain_text = _padding(plain_text, mode=SM4_ENCRYPT)
    if plain_text is None:
        return

    # 密钥检验
    # key = _key_iv_check(key_iv=key)
    # 初始化向量监测
    # iv = _key_iv_check(key_iv=iv)

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
    # .decode('UTF8')
    # return cipher_text if PY2 else cipher_text, (end - start) * 1000
    return cipher_text, (end - start) * 1000


def decrypt_cbc(cipher_text, key, iv):
    """
    SM4(CBC)解密
    :param cipher_text: 密文
    :param key: 密钥 小于等于16字节
    :param iv: 初始化向量 小于等于16字节
    """
    start = time.perf_counter()
    cipher_text = b64decode(cipher_text)
    cipher_hex = _hex(cipher_text)

    # 密钥检测
    # key = _key_iv_check(key_iv=key)
    # 初始化向量检测
    # iv = _key_iv_check(key_iv=iv)
    ivs = [int(_hex(iv), 16)]
    plain_hex_list = []
    for i in range(len(cipher_text) // BLOCK_BYTE):
        sub_hex = cipher_hex[i * BLOCK_HEX:(i + 1) * BLOCK_HEX]
        cipher = int(sub_hex, 16)
        plain = (ivs[i] ^ decrypt(cipher_num=cipher,
                                  mk=int(_hex(key), 16)))
        ivs.append(cipher)
        plain_hex_list.append(num2hex(num=plain, width=BLOCK_HEX))

    plain_text = _padding(_unhex(''.join(plain_hex_list)),
                          mode=SM4_DECRYPT)
    end = time.perf_counter()
    # .decode('UTF8')
    # return plain_text if PY2 else plain_text, (end - start) * 1000
    return plain_text, (end - start) * 1000
