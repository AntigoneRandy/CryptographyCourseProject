# SM4优化调研

## 1 硬件实现优化

SM4密码算法作为国家密码局批准的对称密码算法具有安全性强、效率高和易于硬件实现等特点，在数据加密方面受到了广泛的关注。但是在面对不同应用场景下，SM4算法的高效实现和部署还有进一步提升和优化的空间。

**在硬件实现方面，大部分都是基于循环架构和流水线架构的。**

资源节约方面一直是主流的优化方向，（本文）提出了一种循环型架构，该设计架构在控制模块的协调下，轮密钥生成模块与加密模块并行执行，能够带来多种优势。首先，轮密钥生成模块产生的新鲜轮密钥直接传递给加密模块进行迭代计算，不需要使用额外的寄存器来存储密钥；其次，两个模块并行执行，当密钥更新时，轮密钥生成模块可以实时计算最新的轮密钥，加密模块无需等待，整个加密过程能够连续进行；最后，轮密钥生成模块和加密模块在整个分组数据加密过程中所需要的时钟循环为常数，能够有效抵抗侧信道攻击。

![循环型架构](https://myh-mdpictures.oss-cn-qingdao.aliyuncs.com/img/image-20230107102714231.png)

性能优化方面，（本文）提出了流水线架构，其中流水线主要应用于加密模块。它增加了轮密钥寄存器，轮密钥生成模块将32个轮密钥存储在寄存器中，每个时钟循环都可以向加密模块输入当前轮密钥，保证流水线加密不间断；另外，流水线加密模块实例化32套迭代加密电路，每套迭代电路间插入寄存器，保证了加密过程流水线运行。由于采用流水线架构，在等待32个时钟时延后，每个时钟循环即可完成一次分组数据加密，加密速度快，吞吐量大。

![流水线架构](https://myh-mdpictures.oss-cn-qingdao.aliyuncs.com/img/image-20230107103147950.png)

```
------------------------本文引用-------------------------
@article{何诗洋 2021 SM4算法的FPGA优化实现方法 ,
author={何诗洋 and 李晖 and 李凤华},
title={ SM4算法的FPGA优化实现方法 },
journal={西安电子科技大学学报（自然科学版）},
year={2021},
volume={48},
number={3},
pages={155-162},
month={6},
}
```

## 2 软件实现优化

目前，关于SM4算法的软件优化实现方面的相关工作不多，多使用查表的方法<span style='color:red;background:yellow'>**[1]**</span>，但由于代替表规模相对较大，CPU在做查表操作时，表中数据在内存和cache之间频繁对换导致查表延时较大，且不利于高效并行加/解密多组消息。此外，查表法无法抵抗缓存-计时侧信道攻击，因此在一定程度上制约了SM4的软件实现性能和安全性。

1997年，Biham<span style='color:red;background:yellow'>**[2]**</span>提出了一种新的对称分组密码快速软件实现方法，核心思想是将处理器视为1bit为单位的单指令多数据处理器，后被称为比特切片（bit slicing），它在64位平台上实现了64组DES消息的并行加解密，将逻辑门个数从理论上需要的132个每比特输出优化到100个每比特输出。

为了提高软件实现速度，国内外许多学者尝试将采用 SIMD（Single Instruction Multiple Dada，单指令多数据）技术用于密码算法的软件实现。A. Adomnicai 和 T. Peyrin <span style='color:red;background:yellow'>**[3]**</span>给出改进的比特切片方法“Fixslicing”，在 ARM 和 RISC-V 平台实现了 AES。2012 年 Intel 推出高级向量指令集（Advanced Vector Extensions，AVX）后，众多学者开始研究如何利用 AVX 指令集加速对称分组密码算法的实现速度，尤其是轻量级密码算法的实现速度。Seiichi Matsuda 和 Shiho Moriai<span style='color:red;background:yellow'>**[4]**</span>利用 AVX 指令集加速切片实现，给出了轻量级密码算法面向云端的实现，将 SSE 指令与比特切片方法结合并应用到 PRESENT/Piccolo，使两者的实现吞吐量分别达到 4.3 cycle/byte 和 4.57 cycle/byte。2013 年，Neves 和 Aumasson<span style='color:red;background:yellow'>**[5]**</span>将 AVX2 指令应用到 SHA-3 候选算法 BLAKE 上并提高了其实现性能。最近，郎欢等<span style='color:red;background:yellow'>**[6]**</span>利用 X86 架构下的 SIMD 指令给出了高效的 SM4 实现，他们采用 C 语言调用 AVX2 指令接口方式实现，在并行查表的基础上，给出了两种不同的方法。2014 年 Kostas Papapagiannopoulos 等人<span style='color:red;background:yellow'>**[7]**</span>将比特切片方法修改为 nibble 切片方法，并减少了访问内存，在 AVR 处理器上给出了高效实现。

此外，研究者们将比特切片方法和其它方法结合，对 SM4 算法进行软件实现，也取得了较好的效果。 SM4 算法公布不久，Fen Liu 等 <span style='color:red;background:yellow'>**[8]**</span>破解了 SM4 算法 S 盒的结构，公布了 S 盒的代数表达式及具体参数值。之后，Hao Liang 等<span style='color:red;background:yellow'>**[9]**</span>基于已破解的 SM4 中 S 盒结构，提出了基于复合域的 SM4 实现方法，将 S 盒的有限域求逆运算变换到复合域中实现，并在 FPGA 上进行验证。Jingbin Zhang 等<span style='color:red;background:yellow'>**[10]**</span>提出了 SM4 在复合域中的软件实现，使用 X86 架构普通指令实现，速率达到 20 Mbps。最近, A. Eldosouky 和 W. Saad<span style='color:red;background:yellow'>**[11]**</span>针对物联网应用的效率、安全需求改进了轻量级密码算法 LED 的比特切片方法，并在嵌入式处理器 ARM Cortex-A53 进行了实现验证。O. Hajihassani 等<span style='color:red;background:yellow'>**[12]**</span>利用比特切片方法进一步提高了高级加密算法 AES 的加解密吞吐率。

```
---------------------------本文引用-----------------------------
@article{张笑从 2020 SM4算法快速软件实现 ,
author={张笑从 and 郭华 and 张习勇 and 王闯 and 刘建伟},
title={ SM4算法快速软件实现 },
journal={密码学报},
year={2020},
volume={7},
number={6},
pages={799-811},
month={12},
}

---------------------------文内引用-----------------------------
[1]
@article{lv2016overview,
  title={Overview on SM4 algorithm},
  author={Lv, S and Su, B and Wang, Peng and Mao, Y and Huo, L},
  journal={Journal of Information Security Research},
  volume={2},
  number={11},
  pages={995--1007},
  year={2016}
}

[2]
@inproceedings{biham1997fast,
  title={A fast new DES implementation in software},
  author={Biham, Eli},
  booktitle={International Workshop on Fast Software Encryption},
  pages={260--272},
  year={1997},
  organization={Springer}
}

[3]
@article{adomnicai2020fixslicing,
  title={Fixslicing AES-like ciphers: New bitsliced AES speed records on ARM-Cortex M and RISC-V},
  author={Adomnicai, Alexandre and Peyrin, Thomas},
  journal={Cryptology ePrint Archive},
  year={2020}
}

[4]
@inproceedings{matsuda2012lightweight,
  title={Lightweight cryptography for the cloud: exploit the power of bitslice implementation},
  author={Matsuda, Seiichi and Moriai, Shiho},
  booktitle={International Workshop on Cryptographic Hardware and Embedded Systems},
  pages={408--425},
  year={2012},
  organization={Springer}
}

[5]
@article{neves2012implementing,
  title={Implementing blake with avx, avx2, and xop},
  author={Neves, Samuel and Aumasson, Jean-Philippe},
  journal={Cryptology ePrint Archive},
  year={2012}
}

[6]
@article{huan2018fast,
  title={Fast software implementation of SM4},
  author={Huan, LANG and Lei, ZHANG and Wenling, WU},
  journal={Journal of University of Chinese Academy of Sciences},
  volume={35},
  number={2},
  pages={180},
  year={2018}
}

[7]
@inproceedings{papapagiannopoulos2014high,
  title={High throughput in slices: the case of PRESENT, PRINCE and KATAN64 ciphers},
  author={Papapagiannopoulos, Kostas},
  booktitle={International Workshop on Radio Frequency Identification: Security and Privacy Issues},
  pages={137--155},
  year={2014},
  organization={Springer}
}

[8]
@inproceedings{liu2007analysis,
  title={Analysis of the SMS4 block cipher},
  author={Liu, Fen and Ji, Wen and Hu, Lei and Ding, Jintai and Lv, Shuwang and Pyshkin, Andrei and Weinmann, Ralf-Philipp},
  booktitle={Australasian Conference on Information Security and Privacy},
  pages={158--170},
  year={2007},
  organization={Springer}
}

[9]
@inproceedings{liang2014design,
  title={Design of a masked S-Box for SM4 based on composite field},
  author={Liang, Hao and Wu, Liji and Zhang, Xiangmin and Wang, Jiabin},
  booktitle={2014 Tenth International Conference on Computational Intelligence and Security},
  pages={387--391},
  year={2014},
  organization={IEEE}
}

[10]
@inproceedings{zhang2018fast,
  title={Fast implementation for SM4 cipher algorithm based on bit-slice technology},
  author={Zhang, Jingbin and Ma, Meng and Wang, Ping},
  booktitle={International Conference on Smart Computing and Communication},
  pages={104--113},
  year={2018},
  organization={Springer}
}

[11]
@inproceedings{eldosouky2018cybersecurity,
  title={On the cybersecurity of m-health iot systems with led bitslice implementation},
  author={Eldosouky, AbdelRahman and Saad, Walid},
  booktitle={2018 IEEE International Conference on Consumer Electronics (ICCE)},
  pages={1--6},
  year={2018},
  organization={IEEE}
}

[12]
@article{hajihassani2019fast,
  title={Fast AES implementation: A high-throughput bitsliced approach},
  author={Hajihassani, Omid and Monfared, Saleh Khalaj and Khasteh, Seyed Hossein and Gorgin, Saeid},
  journal={IEEE Transactions on parallel and distributed systems},
  volume={30},
  number={10},
  pages={2211--2222},
  year={2019},
  publisher={IEEE}
}

```

