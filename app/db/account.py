from app import c, conn, logger
from config import max_on_account


def check_funds(sender, amount):
    try:
        c.execute("select balance from accounts where user_id='{}'".format(sender))
        balance = c.fetchone()[0]
        if balance - amount >= 0:
            return True
        else:
            return False
    except conn.Error as e:
        logger.error("Database Error %s", e)
        return None


def transfer(sender, receiver, amount):
    try:
        # stored procedure locates in test_data.sql
        c.execute("select transfer('{}', '{}', {}, {})".format(sender, receiver, amount, max_on_account))
        result = c.fetchone()
        conn.commit()
        return result
    except conn.Error as e:
        logger.error("Database Error %s", e)
        conn.rollback()
        return None


def get_current(sender):
    try:
        c.execute("select balance from accounts where user_id='{}'".format(sender))
        balance = c.fetchone()[0]
        return balance
    except conn.Error as e:
        logger.error("Database Error %s", e)
        return None
    except TypeError as e:
        logger.error("TypeError Error %s. No account for user %s", e, sender)
        return None