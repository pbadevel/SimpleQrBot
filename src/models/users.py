from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.enums import UserRole
from src.kit.models import RecordModel



class User(RecordModel):

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    first_name: Mapped[str]
    last_name: Mapped[str | None]

    username: Mapped[str | None] = mapped_column(unique=True)

    role: Mapped[str] = mapped_column(default=UserRole.USER)

    qr_is_used: Mapped[bool] = mapped_column(default=False)

    @property
    def fullname(self):
        return self.first_name + (" " + self.last_name if self.last_name else "")
    
    @property
    def link_to_user(self):
        if self.username:
            return f"https://t.me/{self.username}"
        return f"tg://user?id={self.id}"
    
    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN 
    
    @property
    def name(self):
        """
        Returns:
            username - if exists, else fullname
        """
        if self.username:
            return f"@{self.username}"
        return self.fullname
