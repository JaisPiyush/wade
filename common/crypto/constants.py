from enum import Enum


class SigningAlgorithm(Enum):
    ED25519 = "ED25519"
    ED448 = "ED448"

class EncryptionAlgorithm(Enum):
    RSA = "RSA"


class HashingAlgorithm(Enum):
    BLAKE2B = "BLAKE2B"