#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import base64

from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad


class AESCipher(object):
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded_plaintext = pad(plaintext.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        iv_ciphertext = base64.b64encode(self.iv + ciphertext).decode('utf-8')
        return iv_ciphertext

    def decrypt(self, ciphertext):
        iv_ciphertext = base64.b64decode(ciphertext)
        iv = iv_ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_padded_text = cipher.decrypt(iv_ciphertext[AES.block_size:])
        decrypted_text = unpad(decrypted_padded_text, AES.block_size).decode('utf-8')
        return decrypted_text


class DESCipher(object):
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, plaintext):
        cipher = DES.new(self.key, DES.MODE_CBC, self.iv)
        padded_plaintext = pad(plaintext.encode(), DES.block_size)
        ciphertext = cipher.encrypt(padded_plaintext)
        iv_ciphertext = base64.b64encode(self.iv + ciphertext).decode('utf-8')
        return iv_ciphertext

    def decrypt(self, ciphertext):
        iv_ciphertext = base64.b64decode(ciphertext)
        iv = iv_ciphertext[:DES.block_size]
        cipher = DES.new(self.key, DES.MODE_CBC, iv)
        decrypted_padded_text = cipher.decrypt(iv_ciphertext[DES.block_size:])
        decrypted_text = unpad(decrypted_padded_text, DES.block_size).decode('utf-8')
        return decrypted_text
