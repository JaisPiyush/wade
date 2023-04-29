# from enum import Enum

# from typing import Optional
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519, ed448, rsa
from cryptography.exceptions import InvalidSignature
import base64
from common.crypto.constants import EncryptionAlgorithm, HashingAlgorithm, SigningAlgorithm
from common.crypto.exception import *

SigningAlgorithmHandlers = {
    SigningAlgorithm.ED25519.value: ed25519.Ed25519PublicKey, # 50
    SigningAlgorithm.ED448.value: ed448.Ed448PublicKey, # 80
}

EncryptionAlgorithmHandlers = {
    EncryptionAlgorithm.RSA.value: rsa.RSAPublicKey, #600
}

HashingAlgorithmHandlers = {
    HashingAlgorithm.BLAKE2B.value: hashes.BLAKE2b
}


SigningPublicKey = ed25519.Ed25519PublicKey | ed448.Ed448PublicKey
EncryptionPublicKey = rsa.RSAPublicKey


class Cryptographer:

    public_key: SigningPublicKey | EncryptionPublicKey | None
    algo: str

    @staticmethod
    def bytes_from_encoded(_string: str) -> bytes:
        return base64.b64decode(_string)
    
    @staticmethod
    def load_signing_key(public_key: str, algo: str) -> SigningPublicKey:
        public_bytes = Cryptographer.bytes_from_encoded(public_key)
        try:
            algorithm = SigningAlgorithmHandlers[algo.upper()]
            return algorithm.from_public_bytes(public_bytes)
        except KeyError:
            raise SigningAlgorithmNotSupported(algo)
    
    @staticmethod
    def load_encryption_key(public_key: str, algo: str) -> EncryptionPublicKey:
        public_bytes = Cryptographer.bytes_from_encoded(public_key)
        try:
            EncryptionAlgorithmHandlers[algo.upper()]
            return load_pem_public_key(public_bytes)
        except KeyError:
            raise EncryptionAlgorithmNotSupported(algo)
    
    def __init__(self, public_key: str, algo: str) -> None:
        self.algo = algo.upper()
        if algo in SigningAlgorithm.__members__.keys():
            self.public_key = Cryptographer.load_signing_key(public_key, self.algo)
        elif algo in EncryptionAlgorithm.__members__.keys():
            self.public_key = Cryptographer.load_encryption_key(public_key, self.algo)
        else:
            raise CryptographyAlgorithmNotSupported(self.algo)
    
    """
    Verifies the signature for a message. The signature must be base64 encoded
    and the message should be plain string
    """
    def verify_signature(self, signature: str, message: str) -> bool:
        if not self.algo in SigningAlgorithm.__members__.keys():
            raise CryptographicOperationNotSupportedForAlgorithm(
                f"{self.algo} does not support signature verification"
            )
        try:
            self.public_key.verify(Cryptographer.bytes_from_encoded(signature), message.encode())
            return True
        except InvalidSignature:
            return False
    """
    Encrypts plain text message and returns base64 encoded string.
    The encryption uses OAEP padding with SHA256 algorithm
    """
    def encrypt(self, message: str) -> str:
        if self.algo not in EncryptionAlgorithm.__members__.keys():
            raise CryptographicOperationNotSupportedForAlgorithm(
                f"{self.algo} does not support message encryption"
            )
        return base64.b64encode(
            self.public_key.encrypt(
                message.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        ).decode()
    
    """
    Returns base64 encoded hash
    """
    @staticmethod
    def digest(algo: HashingAlgorithm, message: str) -> str:
        digest = hashes.Hash(HashingAlgorithmHandlers[algo.value](64))
        digest.update(message.encode())
        return base64.b64encode(digest.finalize()).decode()
        

    

        