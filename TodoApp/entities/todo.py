from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from ..context.database import Base


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, nullable=False)
    complete = Column(Boolean, default=False, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))
