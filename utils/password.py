from hashlib import pbkdf2_hmac
from secrets import randbits
from typing import Tuple


class Password():

    @staticmethod
    def salt_shaker() -> bytes:
        """Generate a salt in the form of a 16-byte array"""
        return randbits(16 * 8).to_bytes(16, "big")

    @staticmethod
    def hash_griddle(pass_text: str) -> Tuple[str, str]:
        """Return a salted hash and the salt strings from a password string."""
        salt = Password.salt_shaker()
        pass_hash = pbkdf2_hmac("sha1", pass_text.encode("utf-8"), salt, 65536,
                                16)
        return pass_hash.hex(), salt.hex()

    @staticmethod
    def check_pass(pass_text: str, pass_hash: str, pass_salt: str) -> bool:
        """Checks if a text string's salted hash matches the stored hash."""
        check_hash = pbkdf2_hmac("sha1", pass_text.encode("utf-8"),
                                 bytes.fromhex(pass_salt), 65536, 16)
        return True if check_hash == bytes.fromhex(pass_hash) else False
