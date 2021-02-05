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
    replace_into_sql = "REPLACE INTO {0} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".format(
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


def save_data_to_postgresql_db(data, host, port, user, password, db_name, table_name):
    """"""

    # Create the table if it does not exist
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
    replace_into_sql = "REPLACE INTO {0} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)".format(
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

            except PostgresqlError as err:
                LOGGER.error("Error in DB: {0}".format(err.args[0]))
