"""
Password Utility Module for EcoGen AI

Provides secure password hashing and verification using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.

    Parameters
    ----------
    password : str
        User password.

    Returns
    -------
    str
        Hashed password.
    """
    try:
        salt = bcrypt.gensalt()

        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            salt,
        )

        return hashed.decode("utf-8")

    except Exception as e:
        raise Exception(f"Password hashing failed: {e}")


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Verify a password against its bcrypt hash.

    Parameters
    ----------
    password : str
        Password entered by user.

    password_hash : str
        Stored bcrypt hash.

    Returns
    -------
    bool
        True if password matches.
    """
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )

    except Exception:
        return False