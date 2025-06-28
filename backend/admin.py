from fastapi import Depends, HTTPException
from models import User

def admin_required(user: User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Adminrechte erforderlich")
    return user

@router.delete("/server/{server_id}")
def delete_server(server_id: int, user: User = Depends(admin_required), db: Session = Depends(get_db)):
    ...
