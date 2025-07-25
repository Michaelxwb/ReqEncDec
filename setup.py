from setuptools import setup, find_packages

setup(
    name='req_enc_dec',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pycryptodome>=3.10.1',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='Request/Response Encryption/Decryption Middleware',
    license='MIT',
    keywords='middleware encryption decryption',
    url='https://github.com/yourusername/req_enc_dec',
)