# Request Encryption/Decryption Middleware

一个 Python 中间件，用于拦截请求和响应，以根据 URL 配置加密/解密特定字段。

## Features

1. **请求解密**：解密传入请求中的指定字段。
2. **响应加密**：加密传出响应中的指定字段。
3. **嵌套字段支持**：使用点符号（例如 `user.data.email`）处理嵌套字段。
4. **可配置加密**：支持多种可逆加密算法和自定义盐值。
5. **即插即用**：易于集成到现有项目中。

## Installation

```bash
pip install req_enc_dec
```

## Usage

```python
from flask import Flask, request

from req_enc_dec import EncryptionPlugin

app = Flask(__name__)

# Configure the middleware
app.config["ENCRYPTION_ALGO"] = "AES"
app.config["ENCRYPTION_SALT"] = b"your_salt_value"
app.config["ENCRYPTION_KEY"] = b'secret_key'
app.config["ENCRYPTION_URL_CONFIGS"] = {
    "/api/user": {
        "decrypt_fields": ["email"],
        "encrypt_fields": ["user.token", "user.list.name", "user.list.email.email_name", "user.list.qq"]
    }
}

EncryptionPlugin(app=app)


@app.route("/api/user", methods=["POST"])
def handle_user():
    request_data = request.get_json()
    print("email: {}".format(request_data.get("email")))
    return {
        "user":
            {
                "token": "test_token",
                "list": [
                    {
                        "name": "test_name01",
                        "email": [
                            {"email_name": "test_email01"},
                            {"email_name": "test_email02"}
                        ],
                        "qq": ["test_qq01", "test_qq02"],
                    },
                    {
                        "name": "test_name02",
                        "email": [],
                        "qq": [],
                    }
                ]
            }
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```

## Configuration
- `ENCRYPTION_ALGO`：要使用的加密算法（默认值：`AES`）。
- `ENCRYPTION_SALT`：用于加密的自定义盐值。
- `ENCRYPTION_URL_CONFIGS`：将 URL 映射到其各自字段配置的字典。
## Supported Algorithms

- `AES`（默认）
- 可以通过扩展中间件添加更多算法。

## License

MIT