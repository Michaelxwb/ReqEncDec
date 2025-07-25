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
        self.config = app.config.copy()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.cipher_instance = self.create_cipher_instance()
        self.register_middleware()

    def create_cipher_instance(self):
        algo = self.config.get("ENCRYPTION_ALGO", "AES")
        key = hashlib.sha256(self.config['ENCRYPTION_KEY']).digest()

        if algo == "AES":
            iv = self.config['ENCRYPTION_SALT'][:AES.block_size].ljust(AES.block_size, b'\0')
            return AESCipher(key[:32], iv)
        elif algo == "DES":
            iv = self.config['ENCRYPTION_SALT'][:DES.block_size].ljust(DES.block_size, b'\0')
            return DESCipher(key[:8], iv)
        else:
            raise ValueError(f"Unsupported encryption algorithm: {algo}")

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
        return self.cipher_instance.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.cipher_instance.decrypt(ciphertext)
