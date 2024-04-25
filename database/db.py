import os

import sqlite3


# ======================================================================================================================


def ensure_connection(func):
    def inner(*args, **kwargs):
        db_file_path = os.path.join(os.path.dirname(__file__), 'DataBase.db')
        with sqlite3.connect(db_file_path) as conn:
            res = func(*args, conn=conn, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    c = conn.cursor()

    if force:
        c.execute("DROP TABLE IF EXISTS domains")
        c.execute("DROP TABLE IF EXISTS subdomains")

    c.execute("""
        CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY,
            domain TEXT,
            notification_status BOOLEAN DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS subdomains (
            id INTEGER PRIMARY KEY,
            domain TEXT,
            subdomain TEXT
        )
    """)


# ======================================================================================================================


@ensure_connection
def get_all_domains(conn, notification_true: bool = False):
    c = conn.cursor()
    if notification_true:
        domains = c.execute("SELECT domain FROM domains WHERE notification_status = ?", (1, )).fetchall()
        return domains

    domains = c.execute("SELECT domain, notification_status FROM domains").fetchall()
    return domains


# ======================================================================================================================


class Domain:
    @staticmethod
    def _ensure_connection(func):
        def inner(self, *args, **kwargs):
            db_file_path = os.path.join(os.path.dirname(__file__), 'DataBase.db')
            with sqlite3.connect(db_file_path) as conn:
                return func(self, conn, *args, **kwargs)

        return inner

    @_ensure_connection
    def __init__(self, conn, domain: str = None, notification_status: int = 0, subdomains_list: list = None):
        c = conn.cursor()
        self.domain = domain

        data = c.execute("SELECT * FROM domains WHERE domain = ?", (self.domain, )).fetchone()
        if data is None:
            self.add_domain()

            self.notification_status = notification_status
        else:
            self.notification_status = int(data[2])

            subdomains_list = c.execute("SELECT * FROM subdomains WHERE domain = ?", (self.domain, )).fetchall()
            self.subdomains = subdomains_list

    @_ensure_connection
    def add_domain(self, conn):
        c = conn.cursor()
        c.execute("INSERT INTO domains (domain) VALUES (?)", (self.domain, ))
        conn.commit()

    @_ensure_connection
    def delete_domain(self, conn):
        c = conn.cursor()
        c.execute("DELETE FROM domains WHERE domain = ?", (self.domain, ))
        c.execute("DELETE FROM subdomains WHERE domain = ?", (self.domain, ))
        conn.commit()

    @_ensure_connection
    def change_domain_status(self, conn):
        c = conn.cursor()
        status = 0
        if self.notification_status == 0:
            status = 1
        c.execute("UPDATE domains SET notification_status = ? WHERE domain = ?", (status, self.domain, ))
        conn.commit()

    @_ensure_connection
    def add_subdomains(self, conn, subdomains: set) -> tuple[bool, set or None]:
        c = conn.cursor()
        c.execute("SELECT subdomain FROM subdomains WHERE domain = ?", (self.domain,))
        existing_subdomains = {row[0] for row in c.fetchall()}

        if not existing_subdomains:
            # If no existing subdomains, add all new ones
            c.executemany("INSERT INTO subdomains (domain, subdomain) VALUES (?, ?)",
                          [(self.domain, subdomain) for subdomain in subdomains])
            conn.commit()
            return True, subdomains

        new_subdomains_set = subdomains
        if existing_subdomains == new_subdomains_set:
            return False, None

        # Only add subdomains that are not already in the database
        subdomains_to_add = new_subdomains_set - existing_subdomains

        if subdomains_to_add:
            c.executemany("INSERT INTO subdomains (domain, subdomain) VALUES (?, ?)",
                          [(self.domain, subdomain) for subdomain in subdomains_to_add])
            conn.commit()
            return True, subdomains_to_add
        return False, None


# ======================================================================================================================


if __name__ == '__main__':
    init_db()
