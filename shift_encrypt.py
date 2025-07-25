import uuid

CODE_BOOK_ENCRYPT = {'q': 'P', 'v': 'p', 'H': 'J', 'G': 'f', 'l': 'b', 'd': 'F', 'b': 'Q', 't': '2', '6': 'q',
                     'F': 'D', 'a': 'e', 'y': 'o', '8': '7', '5': '9', 'C': 'U', '9': 't', 'X': 'x', '1': 'j',
                     'p': 'z', 'x': 'y', 'E': 'N', 'W': 'R', '3': 'V', '2': 'K', 'c': 'C', 'm': 'T', '0': 'g',
                     'N': 'I', 'O': 'Y', 'A': 'r', 'P': '8', 'U': 'm', '7': 'n', 'K': 'O', 'I': 'Z', 'V': '3',
                     'R': 'v', 'r': '6', 'f': 'l', 'k': 'E', 'z': 'c', 'D': 'G', '4': 'X', 'J': 'M', 'u': '0',
                     'o': '4', 'i': 'L', 's': 'W', 'w': 'k', 'e': 'h', 'j': 'w', 'M': 'u', 'L': 'S', 'n': 'B',
                     'S': 'H', 'B': 'd', 'g': '1', 'T': '5', 'Q': 'i', 'h': 'a', 'Z': 'A', 'Y': 's'}

CODE_BOOK_DECRYPT = {'P': 'q', 'p': 'v', 'J': 'H', 'f': 'G', 'b': 'l', 'F': 'd', 'Q': 'b', '2': 't', 'q': '6',
                     'D': 'F', 'e': 'a', 'o': 'y', '7': '8', '9': '5', 'U': 'C', 't': '9', 'x': 'X', 'j': '1',
                     'z': 'p', 'y': 'x', 'N': 'E', 'R': 'W', 'V': '3', 'K': '2', 'C': 'c', 'T': 'm', 'g': '0',
                     'I': 'N', 'Y': 'O', 'r': 'A', '8': 'P', 'm': 'U', 'n': '7', 'O': 'K', 'Z': 'I', '3': 'V',
                     'v': 'R', '6': 'r', 'l': 'f', 'E': 'k', 'c': 'z', 'G': 'D', 'X': '4', 'M': 'J', '0': 'u',
                     '4': 'o', 'L': 'i', 'W': 's', 'k': 'w', 'h': 'e', 'w': 'j', 'u': 'M', 'S': 'L', 'B': 'n',
                     'H': 'S', 'd': 'B', '1': 'g', '5': 'T', 'i': 'Q', 'a': 'h', 'A': 'Z', 's': 'Y'}


class ShiftCipher(object):
    def __init__(self, key):
        self.input_offset = len(str(key))
        self.__len = None
        self.__offset = 0
        self.new_list = list()
        self.encrypt_dict = CODE_BOOK_ENCRYPT
        self.decrypt_dict = CODE_BOOK_DECRYPT

    def encrypt(self, plaintext: str):
        self.__len = len(plaintext)
        # 计算最终的偏移量
        self.__offset = self.input_offset if self.input_offset < self.__len else self.input_offset % self.__len
        # 根据偏移量生成列表数据
        self.new_list = list(plaintext[self.__len - self.__offset:] + plaintext[0:self.__len - self.__offset])
        # 反转列表数据
        self.new_list.reverse()
        # 根据加密字典加密
        new_content_list = [self.encrypt_dict.get(item, item) for item in self.new_list]
        return ''.join(new_content_list)

    def decrypt(self, plaintext: str):
        self.__len = len(plaintext)
        # 计算最终的偏移量
        self.__offset = self.input_offset if self.input_offset < self.__len else self.input_offset % self.__len
        # 根据解密字典解密
        self.new_list = [self.decrypt_dict.get(item, item) for item in list(plaintext)]
        # 反转列表数据
        self.new_list.reverse()
        # 根据偏移量生成列表数据
        new_plaintext = self.new_list[self.__offset:] + self.new_list[0:self.__offset]
        return ''.join(new_plaintext)


if __name__ == '__main__':
    shift_coll = ShiftCipher(offset=56)
    for i in range(0, 10):
        content = "{}{}{}".format(str(uuid.uuid4()), "s00000", str("3242234"))
        ret1 = shift_coll.encrypt(content)
        # print(ret1)
        ret2 = shift_coll.decrypt(ret1)
        print("明文：{}， 密文：{}，解密是否成功：{}".format(content, ret1, content == ret2))
