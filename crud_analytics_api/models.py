from datetime import datetime

from sqlalchemy import registry, func
from sqlalchemy.orm import Mapped, mapped_column


table_registry = registry()

@table_registry.mapped_as_dataclass
class Sale():
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    sale: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
