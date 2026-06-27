from auth.password_utils import (
    hash_password,
    verify_password,
)

password = "EcoGen@123"

hashed = hash_password(password)

print("Hash:")
print(hashed)

print()

print("Correct Password:")
print(verify_password(password, hashed))

print()

print("Wrong Password:")
print(verify_password("123456", hashed))