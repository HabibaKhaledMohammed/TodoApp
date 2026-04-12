from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from Services.auth_service import get_current_user
from context.database import get_db

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
