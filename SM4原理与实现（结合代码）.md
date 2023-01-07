# SM4原理与实现（结合代码）

## 0.参数

```python
S_BOX = {
    0X00: 0XD6, 0X01: 0X90, 0X02: 0XE9, 0X03: 0XFE, 0X04: 0XCC, 0X05: 0XE1, 0X06: 0X3D, 0X07: 0XB7,
    ......
}

# 系统参数FK
FK = (0XA3B1BAC6, 0X56AA3350, 0X677D9197, 0XB27022DC)

# 固定参数CK
CK = (0X00070E15, 0X1C232A31, 0X383F464D, 0X545B6269,
      ......)

# 轮密钥缓存
_rk_cache = {}

# 加密
SM4_ENCRYPT = 1
# 解密
SM4_DECRYPT = 0
# 分组byte数
BLOCK_BYTE = 16
BLOCK_HEX = BLOCK_BYTE * 2
```

## 1.密钥扩展轮函数

将密钥mk分成四个字段：mk0, mk1, mk2, mk3，每个 32 bit，然后与系统参数FK作异或运算，即
$$
keys=[K0,K1,K2,K3]=[mk0\oplus FK[0],mk1\oplus FK[1],mk2\oplus FK[2],mk3\oplus FK[3]]
$$
然后把这 4 个 K 作为输入，其中 K1, K2, K3 要和固定参数CK作异或，异或的结果送入函数 $\_rep\_t\_s$。在函数 $\_rep\_t\_s$ 中，需要经过两步：非线性变换（函数 $\_non\_linear\_map$ ）和线性变换 $L'$ （函数 $\_linear\_map\_s$）。首先，在 $\_non\_linear\_map$ 中，会将输入分为 4 个字段，每个字段 8 bit，高 4 bit 对应 S 盒的行号，低 4 bit 对应 S 盒的列号，返回 S 盒对应的参数。接下来进入函数 $\_linear\_map\_s$，将输入的 32 位数据与它循环左移 13 位、循环左移 23 位的数据进行异或，最后的结果就是函数 $\_rep\_t\_s$ 的返回值。把这个返回值和最开始的 K0 进行异或，就是一个轮密钥 rk 了。

之后，把本轮输入的 K1, K2, K3 作为下一轮输入的 K0, K1, K2，而把本轮产生的轮密钥 rk 作为下一轮输入的 K3 。

上面这两段的过程要重复 32 次，共产生 32 个轮密钥。

**每一次的流程图如下**

![image-20230102152609861](https://myh-mdpictures.oss-cn-qingdao.aliyuncs.com/img/image-20230102152609861.png)

```python
# 非线性变换，获取S盒对应位置的参数
def _non_linear_map(byte_array):
    return (_s_box(byte_array[0]), _s_box(byte_array[1]),
            _s_box(byte_array[2]), _s_box(byte_array[3]))

# 线性变换L'，把自己和循环左移13位和23位的自己做一个异或运算
def _linear_map_s(byte4):
    _left = loop_left_shift
    return byte4 ^ _left(byte4, 13) ^ _left(byte4, 23)

# 函数F'
def _rep_t_s(byte4):
    # 非线性变换
    b_array = _non_linear_map(_byte_unpack(byte4))
    # 线性变换L'
    return _linear_map_s(_byte_pack(b_array))

def _round_keys(mk):
    _rk_keys = _rk_cache.get(mk)
    if _rk_keys is None:
        mk0, mk1, mk2, mk3 = _byte_unpack(mk, byte_n=16)
        # 与系统参数FK异或
        keys = [mk0 ^ FK[0], mk1 ^ FK[1], mk2 ^ FK[2], mk3 ^ FK[3]]
        for i in _range(32):
            # 获取轮密钥，共32个
            rk = keys[i] ^ _rep_t_s(
                keys[i + 1] ^ keys[i + 2] ^ keys[i + 3] ^ CK[i])
            # 每一轮把产生的轮密钥rk加到keys的后面
            keys.append(rk)
        # 相当于一个滑动窗口，每一轮过去，就向后移动一次，这样就可以把rk作为下一次的最后一个输入，而把这次的K0扔掉。起平移的作用。
        _rk_keys = keys[4:]
        _rk_cache[mk] = _rk_keys
    return _rk_keys
```

## 2.加密

数据分组长度为 128 bit，密钥长度为 128 bit。加密算法采用 32 轮迭代结构，每轮使用一个 32 bit 的轮密钥。

这一块的方法和上面的轮密钥产生比较像，主体是轮函数 $F$ 。

在轮函数 $F$ 中，一组明文 128 bit，分为 4 个字段：X0, X1, X2, X3，每个字段 32 bit，作为一次加密的输入。X1, X2, X3 要与一个轮密钥 rk 作异或，将结果作为函数 $\_rep\_t$ 的输入。在函数 $\_rep\_t$ 中，将刚刚的输入分为 4 个字段，每个字段 8 bit，经过非线性变换（函数 $\_non\_linear\_map$ ）和线性变换 $L$ （函数 $\_linear\_map$）。和上面很像，在函数 $\_non\_linear\_map$ 中，根据高低位的行号列号找到 S 盒的参数，然后再在函数 $\_linear\_map$ 做线性变换。这里的线性变换有所不同，操作是 5 个字段的异或，分别是：输入，输入循环左移 2 位，输入循环左移 10 位，输入循环左移 18 位，输入循环左移 24 位。最后的结果就是函数 $\_rep\_t$ 的返回值，把这个返回值和最开始输入的 X0 异或，就得到一个中间结果了。

之后和轮密钥产生的时候如出一辙，把本轮输入的 X1, X2, X3 作为下一轮输入的 X0, X1, X2，而把本轮产生的中间结果作为下一轮输入的 X3。

上面的这两段过程要重复 32 次，最后产生的那个“中间结果”就是本轮明文分组对应的密文了。

**每一次的流程图如下**

![image-20230102161022490](https://myh-mdpictures.oss-cn-qingdao.aliyuncs.com/img/image-20230102161022490.png)

```python
# 非线性变换，获取S盒对应位置的参数
def _non_linear_map(byte_array):
    return (_s_box(byte_array[0]), _s_box(byte_array[1]),
            _s_box(byte_array[2]), _s_box(byte_array[3]))

# 线性变换L，把自己和循环左移2位、10位、18位和24位的自己做一个异或运算
def _linear_map(byte4):
    _left = loop_left_shift
    return byte4 ^ _left(byte4, 2) ^ _left(byte4, 10) ^ _left(byte4, 18) ^ _left(byte4, 24)

def _rep_t(byte4):
    # 非线性变换
    b_array = _non_linear_map(_byte_unpack(byte4))
    # 线性变换L
    return _linear_map(_byte_pack(b_array))

def _round_f(byte4_array, rk):
    """
    :param rk: 轮密钥, 4byte, 32bit
    """
    x0, x1, x2, x3 = byte4_array
    return x0 ^ _rep_t(x1 ^ x2 ^ x3 ^ rk)

def _crypt(num, mk, mode=SM4_ENCRYPT):
    """
    SM4加密和解密
    :param num: 密文或明文 16byte
    :param mk:  密钥 16byte
    :param mode: 轮密钥顺序
    """
    # 把明文/密文存成列表
    x_keys = list(_byte_unpack(num, byte_n=16))
    # 把轮密钥rk存好
    round_keys = _round_keys(mk)
    # 这个是判断参数的，判断需要加密还是解密。如果是解密，则需要把上面存好的轮密钥rk反序一下。
    if mode == SM4_DECRYPT:
        round_keys = round_keys[::-1]
    for i in _range(32):
        # 这一步做32次，每一次按顺序取4个字，再和一个轮密钥执行轮函数F
        x_keys.append(_round_f(x_keys[i:i + 4], round_keys[i]))
    return _byte_pack(x_keys[-4:][::-1], byte_n=16)
```

