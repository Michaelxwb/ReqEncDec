from flask import Flask, request

from req_enc_dec import EncryptionPlugin
from shift_encrypt import ShiftCipher

app = Flask(__name__)

# Configure the middleware
app.config["ENCRYPTION_ALGO"] = "MY_CUSTOM_ALGO"
app.config["ENCRYPTION_SALT"] = b"your_salt_value"
app.config["ENCRYPTION_KEY"] = b'secret_key'
app.config["ENCRYPTION_URL_CONFIGS"] = {
    "/api/user": {
        "decrypt_fields": ["email"],
        "encrypt_fields": ["user.token", "user.list.name", "user.list.email.email_name", "user.list.qq"]
    }
}

plugin = EncryptionPlugin(app)
plugin.register_cipher("MY_CUSTOM_ALGO", ShiftCipher)


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


#

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
