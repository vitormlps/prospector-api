#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
from fastapi import Depends

# ### Local deps
# from .authentication import IdentityProvider
from ..utils.exception_handlers import throw_auth_error



# def get_current_user(token: str = Depends(IdentityProvider.oauth2_scheme)):
#     return IdentityProvider.check_token_signature(token)


def get_current_user():
    pass


# def get_current_user_admin(token: str = Depends(IdentityProvider.oauth2_scheme)):
#     token_info = IdentityProvider.check_token_signature(token)

#     if 'administrator' not in token_info['realm_access']['roles']:
#         throw_auth_error("Invalid credentials")

#     return token_info


def get_current_user_admin():
    pass
