# security.py
'''
This module provides security-related functions for password hashing and JWT token management.
- using Aragon2-OWASP's recommended password hashing algorithm
Parameters:

1- time_cost: The amount of time (in seconds) that the hashing function will take. 
    1- Higher values increase security 
    2- but also increase the time it takes to hash passwords.
2- memory_cost: The amount of memory (in kilobytes) that the hashing function will use. 
    - Higher values increase security 
    - but also increase the memory usage of the hashing process.
3-- parallelism: The number of parallel threads that the hashing function will use. 
    - Higher values increase security 
    - but also increase the CPU usage of the hashing process.
'''

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

'''
THE HASHER INSTANCE
These parameters implement the OWASP recommendation:
    1- memory_cost = 65536  → 64MB RAM required per hash
    2- time_cost   = 3      → 3 iterations through memory
    3- parallelism = 1      → 1 thread

'''
# Step-1:  Initialize the PasswordHasher with recommended parameters
ph = PasswordHasher(
    time_cost = 3, 
    memory_cost = 65536,
    parallelism = 1
)

#Step-2: Function to hash a password
def hash_password(plain_password: str) -> str:
    """
    Hashes a plain text password using Argon2id.
    Returns a unique hash string every time.
    Note: Returns a unique hash string for identical passwords — because of the random salt.
    """
    return ph.hash(plain_password)

# Step-3: Function to verify a password against a hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.
    Returns True if the password is correct, False otherwise.
    """
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except (VerifyMismatchError, VerificationError):
        return False