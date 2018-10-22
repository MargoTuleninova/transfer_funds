from app.db.user import check_login_credentials
from functools import wraps
from flask import request, abort
import re
from app import logger


reg = re.compile('(\w+)[:=] ?"?(\w+)"?')


def check_auth():
    # header - Authorization: Basic login=value password=value
    header = request.headers.get("Authorization", None)
    if not header:
        logger.warning("Authorization header is not provided")
        return False
    header = dict(reg.findall(header))
    if header.get("login") and header.get("password"):
        return check_login_credentials(header["login"], header["password"])
    else:
        logger.warning("Authorization header has wrong format %s", header)
        return False
