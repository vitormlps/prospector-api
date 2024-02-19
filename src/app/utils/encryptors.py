#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ### Built-in deps
# ### Third-party deps
import bcrypt

# ### Local deps


def encrypt_pw(raw_pw: str) -> str:
    return bcrypt.hashpw(raw_pw.encode(), bcrypt.gensalt()).decode()
