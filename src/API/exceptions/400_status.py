from fastapi import HTTPException


invalid_credentials_401 = HTTPException(
    status_code=401, 
    detail="Incorrect login or password."
    )

code_required_403 =  HTTPException(
    status_code=403, 
    detail="Code required. Please POST it to this endpoint with 'code'."
    )
                       
user_not_found_404 = HTTPException(
    status_code=404, 
    detail="User not found."
    )           
        
two_factor_required_403 =  HTTPException(
    status_code=403, 
    detail="Two-factor authentication required."
    )          
      
too_many_attempts_429 = HTTPException(
    status_code=429, 
    detail="Too many login attempts. Please wait."
    )
                   
relogin_exceeded_429 =  HTTPException(
    status_code=429, 
    detail="Relogin attempts exceeded."
    )
            
internal_server_error_500 = HTTPException(
    status_code=500, 
    detail=f"Unexpected error: {str(e)}"
    )