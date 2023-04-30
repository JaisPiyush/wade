from nacl.public import PublicKey, SealedBox


class X25519PublicKey:

    public_key: PublicKey
    sealed_box: SealedBox

    def __init__(self, public_bytes: bytes) -> None:
        self.public_key = PublicKey(public_bytes)
        self.sealed_box = SealedBox(self.public_key)
    
    @classmethod
    def from_public_bytes(cls, public_bytes: bytes) -> "X25519PublicKey":
        return cls(public_bytes)
    
    def encrypt(self, message_bytes: bytes) -> bytes:
        return self.sealed_box.encrypt(message_bytes)
    
    def public_bytes(self, *args, **kwargs) -> bytes:
        return self.public_key._public_key
    
