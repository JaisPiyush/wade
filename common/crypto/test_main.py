from unittest import TestCase
from .main import *
from .exception import *


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, ed448

class TestCryptographer(TestCase):

    def serialize_public_key(self, public_key: ed25519.Ed25519PublicKey | ed448.Ed448PublicKey) -> str:
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return f"0x{public_bytes.hex()}"

    def test_loading_of_algorithm_fail(self):
        xEd25519_key = ed25519.Ed25519PrivateKey.generate()
        public_key = self.serialize_public_key(xEd25519_key.public_key())
        self.assertRaises(
            CryptographyAlgorithmNotSupported,
            Cryptographer,
            public_key, "ecdsa"
        )
    
    def test_loading_of_signing_algo_ed25519_pass(self):
        xEd25519_key = ed25519.Ed25519PrivateKey.generate()
        public_key = self.serialize_public_key(xEd25519_key.public_key())
        loaded_public_key = Cryptographer(public_key, SigningAlgorithm.ED25519.value)
        self.assertEqual(self.serialize_public_key(loaded_public_key.public_key), 
                         self.serialize_public_key(xEd25519_key.public_key()))
    
    def test_loading_of_signing_alog_ed448_pass(self):
        xEd448_key = ed448.Ed448PrivateKey.generate()
        public_key = self.serialize_public_key(xEd448_key.public_key())
        loaded_public_key = Cryptographer(public_key, SigningAlgorithm.ED448.value)
        self.assertEqual(self.serialize_public_key(loaded_public_key.public_key), 
                         self.serialize_public_key(xEd448_key.public_key()))




