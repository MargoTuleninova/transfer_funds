from unittest import TestCase, main
from app.db.account import get_current, check_funds, transfer
from app.db.user import get_id_by_phone, check_login_credentials


class Test(TestCase):
    sender = '539d06fc-63c1-49d4-b321-d88f45f4bef6'
    sender_phone = 79250000000
    sender_login = 'alice'
    sender_pwd = '12345678'
    receiver = '4e422ac0-5847-43b2-b8dd-c3a94c602e9e'
    amount = 10

    # def setUp(self):
        # TODO: make sql file repeatable (if not exists, upsert schemas)
        # with c as cursor:
        #     cursor.execute(open("schema.sql", "r").read())

    def test_get_current_for_existing_user(self):
        self.assertIsNotNone(get_current(self.sender))

    def test_check_funds(self):
        self.assertTrue(check_funds(self.sender, self.amount))

    def test_transfer(self):
        self.assertTrue(transfer(self.sender, self.receiver, self.amount))
        self.assertTrue(transfer(self.receiver, self.sender, self.amount))

    def test_get_id_by_phone(self):
        self.assertIsNotNone(get_id_by_phone(self.sender_phone))

    def test_check_login_credentials(self):
        self.assertTrue(check_login_credentials(self.sender_login, self.sender_pwd))

    # TODO: negative tests


if __name__ == '__main__':
    main()
