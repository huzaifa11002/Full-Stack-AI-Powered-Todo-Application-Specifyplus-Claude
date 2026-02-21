"""Password hashing and verification utilities using the bcrypt library directly.

This module provides functions for:
- Hashing passwords with bcrypt (cost factor 12)
- Verifying passwords against bcrypt hashes
- Handling the 72-byte limit consistently
"""

import bcrypt

def _truncate_password(password: str) -> bytes:
    """Truncate password to 72 bytes and return as bytes for bcrypt.
    
    Bcrypt has a hard limit of 72 bytes. This function safely truncates
    passwords at UTF-8 character boundaries.
    """
    password_bytes = password.encode('utf-8')
    if len(password_bytes) <= 72:
        return password_bytes
    
    # Truncate to 72 bytes and handle UTF-8 character boundaries
    truncated = password_bytes[:72]
    # Decode and re-encode to ensure no partial characters at the boundary
    return truncated.decode('utf-8', errors='ignore').encode('utf-8')

def hash_password(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Bcrypt hashed password as a string
    """
    # 1. Truncate and convert to bytes
    password_bytes = _truncate_password(password)
    
    # 2. Generate salt and hash
    # rounds=12 is a good balance between security and performance
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # 3. Return as string for database storage
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(f"DIAGNOSTIC: verify_password called with direct bcrypt module for password length: {len(plain_password)}")
    try:
        # 1. Truncate and convert to bytes
        password_bytes = _truncate_password(plain_password)
        
        # 2. Convert hash string back to bytes for comparison
        hash_bytes = hashed_password.encode('utf-8')
        
        # 3. Check password
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except Exception as e:
        # If there's any error in format, it's an invalid password/hash
        print(f"Error during password verification: {e}")
        return False