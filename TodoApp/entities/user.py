from sqlalchemy import Boolean, Column, Integer, String
from context.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=True)
    fullname = Column(String, nullable=True)
    hashed_password= Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    role= Column(String, nullable=True)
    phone_number= Column(String, nullable=True)
