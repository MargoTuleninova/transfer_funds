from app.auth import check_auth
from flask import request
from app import logger
from config import max_on_account
from app.db.user import get_id_by_phone
from app.db.account import check_funds, transfer, get_current
from app.routes import routes
from json import dumps


@routes.route("/", methods=['POST'])
def transfer_funds():
    # TODO: request unique id required
    logger.info("New incoming request for transfer")
    # Not secure authorization
    # For simplicity use authorization header as Authorization: Basic login password
    snd_id = check_auth()
    if not snd_id:
        logger.warning("Wrong login or password")
        return "Wrong login or password", 401

    # Getting values of receiver and amount from form
    try:
        rcv_phone = int(request.form.get("Receiver"))
        amount = int(request.form.get("Amount"))
    except (ValueError, TypeError) as e:
        logger.warning("Error getting receiver phone or amount from form. %s", e)
        return '', 400

    # TODO: phone validation
    # simple amount validation
    if amount <= 0 or amount > max_on_account:
        logger.warning("Wrong amount provided. Amount %s", amount)
        return 'Provided amount is not valid', 400

    # Getting receiver info by provided phone
    rcv_id = get_id_by_phone(rcv_phone)
    if not rcv_id:
        logger.warning("Wrong phone number provided: no client with phone %s", rcv_phone)
        return "There is no client with such phone number", 400

    # Checking if sender has enough funds
    # Request is not actually required, while transfer will not proceed if sender has no funds
    # Making for user-friendly response
    if not check_funds(snd_id, amount):
        logger.warning("Not enough funds for transferring")
        return "There is not enough funds on the account", 403

    # Transferring funds
    if not transfer(snd_id, rcv_id, amount):
        logger.error("Transfer fails")
        return '', 500

    logger.info("Transfer success")
    return '', 200


@routes.route("/", methods=['GET'])
def get_funds():
    logger.info("New incoming request for getting funds")
    snd_id = check_auth()
    if not snd_id:
        logger.warning("Wrong login or password")
        return "Wrong login or password", 401
    balance = get_current(snd_id)
    if not balance:
        return '', 500
    return dumps({'balance': balance})