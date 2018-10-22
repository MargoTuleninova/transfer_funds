from app import conn, c
from hashlib import md5
from app import logger


def get_id_by_phone(phone):
    try:
        c.execute("SELECT * FROM users WHERE phone='{}'".format(phone))
        result = c.fetchone()
    except conn.Error as e:
        logger.error("Database Error %s", e)
        return None
    if not result:
        logger.warning("There isn't any client with such phone %s", phone)
        return None
    return result[0]


def check_login_credentials(login, password):
    try:
        c.execute("SELECT id, password, salt from users WHERE login='{}'".format(login))
        result = c.fetchone()
    except conn.Error as e:
        logger.error("Database Error %s", e)
        return None
    if not result:
        logger.warning("There isn't any client with such username %s", login)
        return None
    # password stores as salted hashes
    hash_pwd = md5((password + result[2]).encode()).hexdigest()
    if hash_pwd == result[1]:
        return result[0]
    else:
        logger.warning("Wrong password provided for user %s", login)
        return False
