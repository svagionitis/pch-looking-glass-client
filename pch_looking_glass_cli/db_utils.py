"""
Useful functions for interactions with a DB
"""

import logging
from datetime import datetime
import os
import sqlite3
from sqlite3 import Error as SqliteError
import psycopg2
from psycopg2 import Error as PostgresqlError

LOGGER = logging.getLogger(__name__)


def save_data_to_sqlite_db(
    data, db_dir, db_filename="ixp-info.db", table_name="ixp_info"
):
    """
    Save data to an Sqlite DB

    data: The data to save.
    db_dir: The directory to save the DB.
    db_filename: The filename of the DB. The default value is "ixp-info.db".
    table_name: The table in DB to save the data. The default value is "ixp_info".
    """
    LOGGER.debug(
        "data: %s, db_dir: %s, db_filename: %s, table_name: %s",
        data,
        db_dir,
        db_filename,
        table_name,
    )

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    data_db_filename = os.path.join(db_dir, db_filename)

    # Create the table if it does not exist
    # See https://sqlite.org/lang_createtable.html
    create_table_sql = "\
        CREATE TABLE IF NOT EXISTS {0} ( \
            ixp TEXT NOT NULL, \
            ixp_city TEXT NOT NULL, \
            ixp_country TEXT NOT NULL, \
            ixp_ip_version TEXT NOT NULL, \
            ixp_local_asn INT, \
            ixp_rib_entries INT, \
            ixp_number_of_peers INT, \
            ixp_number_of_neighbors INT, \
            date_added TEXT, \
            PRIMARY KEY (ixp, ixp_city, ixp_country) \
        )".format(
        table_name
    )
    # See https://www.sqlite.org/lang_replace.html
    replace_into_sql = "REPLACE INTO {0} \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".format(
        table_name
    )

    with sqlite3.connect(data_db_filename) as conn:

        curs = conn.cursor()

        try:
            curs.execute(create_table_sql)

            if data:
                curs.execute(
                    replace_into_sql,
                    [
                        data["ixp"],
                        data["ixp_city"],
                        data["ixp_country"],
                        data["ixp_ip_version"],
                        data["ixp_local_asn"],
                        data["ixp_rib_entries"],
                        data["ixp_number_of_peers"],
                        data["ixp_number_of_neighbors"],
                        datetime.utcnow().isoformat(),
                    ],
                )

        except SqliteError as err:
            LOGGER.error("Error in DB: {0}".format(err.args[0]))
        finally:
            if curs:
                curs.close()


def save_data_to_postgresql_db(
    data,
    host="127.0.0.1",
    port=5432,
    user="ixp",
    password="PchL00k1ngGl@ss",
    db_name="ixp",
    table_name="ixp_info",
):
    """
    Save data to an Sqlite DB

    data: The data to save.
    host: The host of the DB. Default value is "127.0.0.1"
    port: The port of the DB. Default value is 5432.
    user: The user to log in to a specific DB with db_name. Default value is "ixp".
    password: The password of the user to log in to a specific DB with db_name. Default value is "PchL00k1ngGl@ss".
    db_name: The name of the DB. The default value is "ixp".
    table_name: The table in DB to save the data. The default value is "ixp_info".
    """

    # Create the table if it does not exist
    # See https://www.postgresql.org/docs/current/sql-createtable.html
    create_table_sql = "\
        CREATE TABLE IF NOT EXISTS {0} ( \
            ixp TEXT NOT NULL, \
            ixp_city TEXT NOT NULL, \
            ixp_country TEXT NOT NULL, \
            ixp_ip_version TEXT NOT NULL, \
            ixp_local_asn INT, \
            ixp_rib_entries INT, \
            ixp_number_of_peers INT, \
            ixp_number_of_neighbors INT, \
            date_added TEXT, \
            PRIMARY KEY (ixp, ixp_city, ixp_country) \
        )".format(
        table_name
    )
    # See https://www.postgresql.org/docs/current/sql-insert.html
    insert_into_sql = "INSERT INTO {0} \
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) \
                       ON CONFLICT (ixp, ixp_city, ixp_country) \
                       DO UPDATE SET ixp_ip_version = EXCLUDED.ixp_ip_version, \
                                     ixp_local_asn = EXCLUDED.ixp_local_asn, \
                                     ixp_rib_entries = EXCLUDED.ixp_rib_entries, \
                                     ixp_number_of_peers = EXCLUDED.ixp_number_of_peers, \
                                     ixp_number_of_neighbors = EXCLUDED.ixp_number_of_neighbors, \
                                     date_added = EXCLUDED.date_added".format(
        table_name
    )

    with psycopg2.connect(
        host=host, port=port, user=user, password=password, dbname=db_name
    ) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(create_table_sql)

                if data:
                    curs.execute(
                        insert_into_sql,
                        [
                            data["ixp"],
                            data["ixp_city"],
                            data["ixp_country"],
                            data["ixp_ip_version"],
                            data["ixp_local_asn"],
                            data["ixp_rib_entries"],
                            data["ixp_number_of_peers"],
                            data["ixp_number_of_neighbors"],
                            datetime.utcnow().isoformat(),
                        ],
                    )

            except PostgresqlError as err:
                LOGGER.error("Error in DB: {0}".format(err.args[0]))
