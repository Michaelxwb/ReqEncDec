#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import copy
import hashlib

from Crypto.Cipher import AES, DES
from flask import request, jsonify

from req_enc_dec.req_crypto import AESCipher, DESCipher


class EncryptionPlugin:
    def __init__(self, app=None):
        self.app = app
        self.config = app.config.copy() if app else {}
        self._cipher_cache = {}
        self._custom_ciphers = {}
        self._cipher_instance = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.register_middleware()

    def create_cipher_instance(self):
        algo = self.config.get("ENCRYPTION_ALGO", "AES")
        key = hashlib.sha256(self.config['ENCRYPTION_KEY']).digest()

        cache_key = f"{algo}_{key.hex()}"
        if cache_key in self._cipher_cache:
            return self._cipher_cache[cache_key]

        if algo in self._custom_ciphers:
            cipher = self._custom_ciphers[algo](key)
        elif algo == "AES":
            iv = self.config['ENCRYPTION_SALT'][:AES.block_size].ljust(AES.block_size, b'\0')
            cipher = AESCipher(key[:32], iv)
        elif algo == "DES":
            iv = self.config['ENCRYPTION_SALT'][:DES.block_size].ljust(DES.block_size, b'\0')
            cipher = DESCipher(key[:8], iv)
        else:
            raise ValueError(
                f"Unsupported encryption algorithm: {algo}. "
                f"Please register it first using `register_cipher` method. "
                f"Registered algorithms: {list(self._custom_ciphers.keys())}"
            )

        self._cipher_cache[cache_key] = cipher
        return cipher

    def register_middleware(self):
        @self.app.before_request
        def before_request():
            url = request.path
            if url in self.config["ENCRYPTION_URL_CONFIGS"] and \
                    self.config["ENCRYPTION_URL_CONFIGS"][url]['decrypt_fields']:
                self.process_nested(request.get_json(), self.config["ENCRYPTION_URL_CONFIGS"][url]['decrypt_fields'],
                                    action='decrypt')

        @self.app.after_request
        def after_request(response):
            url = request.path
            if url in self.config["ENCRYPTION_URL_CONFIGS"] and \
                    self.config["ENCRYPTION_URL_CONFIGS"][url]['encrypt_fields']:
                data = response.get_json()
                encrypted_data = self.process_nested(data, self.config["ENCRYPTION_URL_CONFIGS"][url]['encrypt_fields'],
                                                     action='encrypt')
                response.set_data(jsonify(encrypted_data).data)
            return response

    def process_nested(self, data, fields, action):
        for field in fields:
            keys = field.split('.')
            self._recursive_process(data, keys, action)
        return data

    def _recursive_process(self, data, keys, action):
        if not keys:
            return

        key = keys[0]
        remaining_keys = keys[1:]

        if isinstance(data, dict):
            if key in data:
                if remaining_keys:
                    self._recursive_process(data[key], remaining_keys, action)
                else:
                    if isinstance(data[key], list):
                        cur_value = [self.encrypt(i) if action == 'encrypt' else self.decrypt(i) for i in
                                     copy.deepcopy(data[key])]
                    else:
                        original_value = str(data[key])
                        cur_value = self.encrypt(original_value) if action == 'encrypt' else self.decrypt(
                            original_value)
                    data[key] = cur_value
        elif isinstance(data, list):
            for item in data:
                self._recursive_process(item, keys, action)

    def encrypt(self, plaintext):
        if self._cipher_instance is None:
            self._cipher_instance = self.create_cipher_instance()
        return self._cipher_instance.encrypt(plaintext)

    def decrypt(self, ciphertext):
        if self._cipher_instance is None:
            self._cipher_instance = self.create_cipher_instance()
        return self._cipher_instance.decrypt(ciphertext)

    def register_cipher(self, algo_name, cipher_class):
        """
        注册自定义对称加密算法
        :param algo_name: 算法名称
        :param cipher_class: 加密类，需实现 encrypt 和 decrypt 方法
        """
        if not hasattr(cipher_class, 'encrypt') or not hasattr(cipher_class, 'decrypt'):
            raise ValueError("Custom cipher class must implement 'encrypt' and 'decrypt' methods.")
        self._custom_ciphers[algo_name] = cipher_class
