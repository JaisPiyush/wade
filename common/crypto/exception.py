
class SigningAlgorithmNotSupported(Exception):
    def __init__(self, algo: str) -> None:
        super().__init__(f"{algo} is not supported for signature verification")

class CryptographyAlgorithmNotSupported(Exception):
    def __init__(self, algo: str) -> None:
        super().__init__(f"{algo} is not  supported")