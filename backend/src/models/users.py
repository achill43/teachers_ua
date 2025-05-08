from db import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserSQL(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"

    def __str__(self) -> str:
        return self.__repr__()
