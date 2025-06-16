
INSERT_TABLE_CONTAINERS = """ INSERT INTO containers (name, encrypted_data) VALUES (?, ?) """

SELECT_CONTAINERS = """ SELECT id, name FROM containers """

SELECT_CONTAINER_CONTENT = """ SELECT encrypted_data FROM containers WHERE id=? """

CREATE_USER_TABLE = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """

CREATE_CONTAINER_TABLE = """ CREATE TABLE IF NOT EXISTS containers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                encrypted_data BLOB NOT NULL
            )
        """

UPDATE_CONTAINER_CONTENT = """  UPDATE containers 
                                SET encrypted_data=? 
                                WHERE id=? """

DELETE_CONTAINER = """ DELETE FROM containers WHERE id=? """

SELECT_CONTAINER_COUNT = """ SELECT count(*) FROM containers """

INSERT_USER = """ INSERT INTO users (password_hash, salt)
                  VALUES (?, ?);
                """

SELECT_USER_PASSWORD = """ SELECT password_hash FROM users """

DROP_CONTAINERS = """ DROP TABLE IF EXISTS containers """
DROP_USERS = """ DROP TABLE IF EXISTS users """
