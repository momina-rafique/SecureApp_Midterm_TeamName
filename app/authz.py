from enum import Enum
from fastapi import Depends, HTTPException, status

class Role(str, Enum):
    admin = "admin"
    user = "user"

# assumes you already have get_current_user() that returns a user with a .role field
def require_role(*roles):
    def inner(user=Depends(get_current_user)):
        if getattr(user, "role", "user") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user
    return inner
