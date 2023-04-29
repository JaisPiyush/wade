# from enum import Enum

# from typing import Optional
# from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, ed448

from common.crypto.constants import EncryptionAlgorithm, SigningAlgorithm
from common.crypto.exception import *

SigningAlgorithmHandlers = {
    SigningAlgorithm.ED25519.value: ed25519.Ed25519PublicKey,
    SigningAlgorithm.ED448.value: ed448.Ed448PublicKey
}


SigningPublicKey = ed25519.Ed25519PublicKey | ed448.Ed448PublicKey

class Cryptographer:

    public_key: SigningPublicKey | None
    algo: EncryptionAlgorithm | SigningAlgorithm

    @staticmethod
    def bytes_from_hex(hex_string: str) -> bytes:
        return bytes.fromhex(hex_string.replace("0x", ""))
    
    @staticmethod
    def load_signing_key(public_key: str, algo: str) -> SigningPublicKey:
        public_bytes = Cryptographer.bytes_from_hex(public_key)
        try:
            algorithm = SigningAlgorithmHandlers[algo.upper()]
            return algorithm.from_public_bytes(public_bytes)
        except KeyError:
            raise SigningAlgorithmNotSupported(algo)
    
    def __init__(self, public_key: str, algo: str) -> None:
        algo = algo.upper()
        if algo in SigningAlgorithm.__members__.keys():
            self.public_key = Cryptographer.load_signing_key(public_key, algo)
            self.algo = SigningAlgorithm[algo]
        else:
            raise CryptographyAlgorithmNotSupported(algo)

        