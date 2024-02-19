#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
from copy import copy

# ### Third-party deps
from keycloak import KeycloakOpenID
from fastapi.security import OAuth2AuthorizationCodeBearer

# ### Local deps
from ..utils.error_handling import throw_auth_error


class IdentityProvider:
    open_id = None
    KEYCLOAK_PUBLIC_KEY = None
    oauth2_scheme = None
    options = {
        "verify_signature": True,
        "verify_aud": False,
        "verify_exp": True
    }

    @staticmethod
    def check_token_signature(token):
        try:
            token_info = IdentityProvider.open_id.decode_token(
                token,
                key=IdentityProvider.KEYCLOAK_PUBLIC_KEY,
                options=IdentityProvider.options
            )
            token_info['access_token'] = token

        except:
            throw_auth_error('Token verification failure')

        return token_info


    @staticmethod
    def refresh_token(token: str, refresh_token: str) -> str:
        token_info = IdentityProvider.check_token_signature(token)
        token_origin = token_info.get('azp')
        
        refresh_id_provider_copy = copy(IdentityProvider.open_id)
        refresh_id_provider_copy.client_id = token_origin

        return refresh_id_provider_copy.refresh_token(refresh_token)['access_token']


def set_auth_provider(settings):
    IdentityProvider.open_id = KeycloakOpenID(
        server_url=settings.KEYCLOAK_BASE_URL,
        client_id=settings.KEYCLOAK_CLIENT_ID,
        realm_name=settings.KEYCLOAK_REALM,
        client_secret_key=settings.KEYCLOAK_CLIENT_SECRET
    )

    IdentityProvider.KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + \
        IdentityProvider.open_id.public_key() + "\n-----END PUBLIC KEY-----"

    IdentityProvider.oauth2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=f"{settings.KEYCLOAK_BASE_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth",
        tokenUrl=f"{settings.KEYCLOAK_BASE_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token",
    )
