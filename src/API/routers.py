# from src.API.api.auth.router import router as auth
from src.API.api.instagram.router import router as instagram


api = '/API/api'

def routers_prefixs_tags():
    return (
        # (auth, f'{api}/auth', ['auth']),
        (instagram, f'{api}/instagram', ['instagram']),
    )