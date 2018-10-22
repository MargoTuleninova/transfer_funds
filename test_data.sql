CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (id uuid PRIMARY KEY default uuid_generate_v4(), login varchar(64), phone bigint, password varchar(32), salt varchar(32));
CREATE TABLE accounts (id uuid PRIMARY KEY default uuid_generate_v4(), balance real, user_id uuid, FOREIGN KEY(user_id) REFERENCES users(id));
-- status field can be complicated, we just want to know success or fail
CREATE TABLE transfer_history (id uuid PRIMARY KEY default uuid_generate_v4(), sender_id uuid, FOREIGN KEY(sender_id) REFERENCES users(id), receiver_id uuid, FOREIGN KEY(receiver_id) REFERENCES users(id), status bool);

-- password 12345678
INSERT INTO users VALUES ('539d06fc-63c1-49d4-b321-d88f45f4bef6', 'alice', 79250000000, '60dbf91d28e47be9de3235576b733402', 'fe9c1b041b202872771142c9b83fea02');
-- password qwerty
INSERT INTO users VALUES ('4e422ac0-5847-43b2-b8dd-c3a94c602e9e', 'bob', 79160000000, '2e600e0f7c33ed85af20abc41735b603', 'c48a87a33aba2aac72c3d8507cf2e6d8');

INSERT INTO accounts VALUES ('dd048057-42a4-4ec2-be78-946ff28f7a81', 10000, '539d06fc-63c1-49d4-b321-d88f45f4bef6');
INSERT INTO accounts VALUES ('d8601faa-0f56-41c8-babc-116f509d90e9', 3000, '4e422ac0-5847-43b2-b8dd-c3a94c602e9e');

CREATE FUNCTION transfer(
  sender_id uuid,
  receiver_id uuid,
  amount real,
  max_amount real,
  OUT result_status bool
) AS $$
DECLARE
  sender_balance real;
  receiver_balance real;
BEGIN
  SELECT INTO sender_balance balance
    FROM accounts
    WHERE user_id = sender_id;

  SELECT INTO receiver_balance balance
    FROM accounts
    WHERE user_id = receiver_id;

  IF sender_balance - amount > 0 AND receiver_balance + amount < max_amount THEN
    UPDATE accounts
      SET balance = balance - amount
      WHERE user_id = sender_id;
    UPDATE accounts
      SET balance = balance + amount
      WHERE user_id = receiver_id;
    INSERT INTO transfer_history
      VALUES (uuid_generate_v4(), sender_id, receiver_id, true)
      RETURNING status
      INTO result_status;
  ELSE
    INSERT INTO transfer_history
      VALUES (uuid_generate_v4(), sender_id, receiver_id, false)
      RETURNING status
      INTO result_status;
  END IF;
END;
$$ LANGUAGE plpgsql;