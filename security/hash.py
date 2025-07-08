from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:

    def __init__(self, password):
        self.password = password

    def hash_password(self):
        return pwd_context.hash(self.password)

    def verify_password(self, stored_password: str):
        return pwd_context.verify(self.password, stored_password)
