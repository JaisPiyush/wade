from unittest import TestCase
from .main import *
from .exception import *

import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import ed25519, ed448, rsa

class TestCryptographerLoading(TestCase):

    @staticmethod
    def serialize_public_key(public_key: ed25519.Ed25519PublicKey | ed448.Ed448PublicKey | rsa.RSAPublicKey) -> str:
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return base64.b64encode(public_bytes).decode()

    def test_loading_of_algorithm_fail(self):
        xEd25519_key = ed25519.Ed25519PrivateKey.generate()
        public_key = TestCryptographerLoading.serialize_public_key(xEd25519_key.public_key())
        self.assertRaises(
            CryptographyAlgorithmNotSupported,
            Cryptographer,
            public_key, "ecdsa"
        )
    
    def test_loading_of_signing_algo_ed25519_pass(self):
        xEd25519_key = ed25519.Ed25519PrivateKey.generate()
        public_key = TestCryptographerLoading.serialize_public_key(xEd25519_key.public_key())
        loaded_public_key = Cryptographer(public_key, SigningAlgorithm.ED25519.value)
        self.assertEqual(TestCryptographerLoading.serialize_public_key(loaded_public_key.public_key), 
                         TestCryptographerLoading.serialize_public_key(xEd25519_key.public_key()))
        
    
    def test_loading_of_signing_alog_ed448_pass(self):
        xEd448_key = ed448.Ed448PrivateKey.generate()
        public_key = TestCryptographerLoading.serialize_public_key(xEd448_key.public_key())
        loaded_public_key = Cryptographer(public_key, SigningAlgorithm.ED448.value)
        self.assertEqual(TestCryptographerLoading.serialize_public_key(loaded_public_key.public_key), 
                         TestCryptographerLoading.serialize_public_key(xEd448_key.public_key()))
        
    
    def test_loading_of_enc_key_rsa_pass(self):
        rsa_key: rsa.RSAPrivateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_bytes = rsa_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1
        )
        public_key = base64.b64encode(public_bytes).decode()
        loaded_public_key = Cryptographer(public_key, EncryptionAlgorithm.RSA.value)
        self.assertEqual(
            public_bytes, loaded_public_key.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.PKCS1
            )
        )
    
class TestCryptographer(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.sign_private_key = ed25519.Ed25519PrivateKey.generate()
        self.encrypt_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.sign_crypto = Cryptographer(
            TestCryptographerLoading.serialize_public_key(self.sign_private_key.public_key()),
            SigningAlgorithm.ED25519.value
        )
        self.enc_crypto = Cryptographer(
            base64.b64encode(
                self.encrypt_private_key.public_key().public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.PKCS1
                )
            ).decode(),
            EncryptionAlgorithm.RSA.value
        )
    
    def test_verify_signature_fail_due_to_wrong_msg(self):
        message = "Hello narniya"
        signature_bytes = self.sign_private_key.sign(message.encode())
        signature_hex = base64.b64encode(signature_bytes).decode()
        self.assertFalse(self.sign_crypto.verify_signature(signature_hex, message + "a"))
    
    def test_verify_signature_fail(self):
        message = "Hello narniya"
        signature_bytes = self.sign_private_key.sign(message.encode())
        signature_hex = base64.b64encode(signature_bytes).decode()
        self.assertTrue(self.sign_crypto.verify_signature(signature_hex, message))
    
    def test_encrypt_fail_wrong_algo(self):
        message = "hello"
        self.assertRaises(
            CryptographicOperationNotSupportedForAlgorithm,
            self.sign_crypto.encrypt,
            message
        )
    
    def test_encrypt_pass(self):
        message = "hello"
        encrypted = self.enc_crypto.encrypt(message)
        encrypted_bytes = base64.b64decode(encrypted)
        decrypted = self.encrypt_private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
            
        )

        self.assertEqual(decrypted.decode(), message)
    
    def test_hash_pass(self):
        message = "Pure"
        digest = hashes.Hash(hashes.BLAKE2b(64))
        digest.update(message.encode())
        expected_hash = base64.b64encode(digest.finalize()).decode()
        self.assertEqual(expected_hash, Cryptographer.digest(HashingAlgorithm.BLAKE2B, message))




