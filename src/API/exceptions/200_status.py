from fastapi import HTTPException


raise HTTPException(
    status_code=200, 
    detail="Code verified and login completed."
    )

raise HTTPException(
    status_code=200, 
    detail="Login successful."
    )