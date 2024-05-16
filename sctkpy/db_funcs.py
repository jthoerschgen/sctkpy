# -*- coding: utf-8 -*-

"""Functions related to managing/retrieving data from the SQLite DB
"""

import csv
import logging
import os
import sqlite3

from .config import db_path, default_roster_csv_path, grade_report_dir

logger = logging.getLogger(__name__)


def create_db_conn() -> sqlite3.Connection:
    """Creates a connection to a SQLite database file.
    - If the file does not exist, one is created.
    - Creates tables if tables do not exist.

    Returns:
        sqlite3.Connection: Connection to SQLite database file
    """
    logger.debug("Creating Database connection")
    conn: sqlite3.Connection = sqlite3.connect(db_path)

    cur = conn.cursor()

    # Enable Foreign Keys
    cur.execute("PRAGMA foreign_keys = ON")
    conn.commit()

    # Create Tables
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS "members" (
            "first_name" TEXT,
            "last_name" TEXT,
            "in_house_out" TEXT,
            "pledge_class" INTEGER,
            PRIMARY KEY(
                "first_name",
                "last_name"
            ) ON CONFLICT REPLACE
        );
        """
    )  # Create Table for members

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS "grades" (
            "name" TEXT,
            "term" TEXT,
            "chapter" TEXT,
            "new_member" TEXT,
            "enroll_hrs" INTEGER,
            "priv_gpa" REAL,
            "priv_cum_gpa" REAL,
            "term_gpa" REAL,
            "term_cum_gpa" REAL,
            "class" TEXT,
            "catalog_num" TEXT,
            "hrs" INTEGER,
            "grade" TEXT,
            "grade_type" TEXT,
            PRIMARY KEY(
                "name",
                "term",
                "class",
                "catalog_num",
                "hrs",
                "grade",
                "grade_type"
            ) ON CONFLICT REPLACE
        );"""
    )  # Create Table for grades
    conn.commit()

    return conn


def load_grades_into_db(rows_to_header: int = 2) -> None:
    """Loads all of the grade data from the grade reports in the
    'gradereports' dir and loads them into a SQLite DB at:
    'sctkpy/db/sctkpy.db'

    Returns: None
    """
    logger.debug("Loading grades into database")
    conn = create_db_conn()
    cur = conn.cursor()

    for csv_file_path in os.listdir(grade_report_dir):
        csv_file_path = os.path.join(grade_report_dir, csv_file_path)
        with open(csv_file_path, "r", encoding="utf-8") as csv_file:
            for _ in range(rows_to_header):  # Skip first rows to get to head
                next(csv_file)
            dr = csv.DictReader(csv_file)
            db_vals = {
                (
                    row["Name"],
                    row["Term"],
                    row["Chapter"],
                    row["New Member"],
                    row["Enroll Hrs"],
                    row["Priv GPA"],
                    row["Priv Cum GPA"],
                    row["Term GPA"],
                    row["Term Cum GPA"],
                    row["Class"],
                    row["Catalog No"],
                    row["Hrs"],
                    row["Grade"],
                    row["Grade Type"],
                )
                for row in dr
            }

        for row in db_vals:
            try:
                logger.debug("Adding row to db: %s", row)
                cur.execute(
                    """
                    INSERT INTO grades (
                        name,
                        term,
                        chapter,
                        new_member,
                        enroll_hrs,
                        priv_gpa,
                        priv_cum_gpa,
                        term_gpa,
                        term_cum_gpa,
                        class,
                        catalog_num,
                        hrs,
                        grade,
                        grade_type
                    )
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
                    """,
                    row,
                )
            except sqlite3.IntegrityError as e:
                logger.error("%s / %s", e, row)
    conn.commit()
    conn.close()
    return


def load_roster_into_db(
    csv_file_path: str | None = None, rows_to_header: int = 3
) -> None:
    """Parses the "greeklife_roster_report.csv" either from a given path or
    via the root of the project directory. Saves the results and inserts/
    updates member information in SQLite.

    Args:
        csv_file_path (str | None, optional):
            Optional path to csv file. Defaults to None.
        rows_to_header (int, optional):
            Rows to skip to get the the header. Defaults to 3.

    Returns: None
    """
    if csv_file_path is None:
        csv_file_path = default_roster_csv_path
    logger.debug("Updating member roster from: %s", csv_file_path)

    conn = create_db_conn()
    cur = conn.cursor()

    with open(csv_file_path, "r", encoding="utf-8") as csv_file:
        for _ in range(rows_to_header):  # Skip first rows to get to head
            next(csv_file)
        dr = csv.DictReader(csv_file)
        db_vals = {
            (
                row["First Name"],
                row["Last Name"],
                row["in/out House"],
            )
            for row in dr
        }

    logger.debug("Cleaning out roster in db")
    cur.execute("DELETE FROM members;")  # Clean out roster
    for row in db_vals:
        logger.debug("Adding member to db: %s", row)
        assert row[2] in (
            "IN",
            "OUT",
        ), f"in/out House status must be either 'IN'/'OUT' not, {row[2]}"
        try:
            cur.execute(
                """
                INSERT INTO members (
                    first_name,
                    last_name,
                    in_house_out
                )
                VALUES (?,?,?);
                """,
                row,
            )
        except sqlite3.IntegrityError as e:
            logger.error("%s / %s", e, row)
    conn.commit()
    conn.close()
    return


def get_files_due_list_db(term: str) -> list[tuple[str, str, str]]:
    """Get data of who is responsible for creating what files.

    Args:
        term (str): Academic term to get data from (FSXXXX/SPXXXX)

    Returns:
        list[tuple[str, str, str]]:
            List of tuples where the tuple contains a class name as a string,
            the course code as a string, and a list of members enrolled in the
            course, who are all responsible for submitting a file, as a csv
            string.
    """
    conn = create_db_conn()
    cur = conn.cursor()

    res = cur.execute(
        """
        SELECT
            DISTINCT class as class_name,
            catalog_num,
            GROUP_CONCAT(DISTINCT name) as names
        FROM grades
        WHERE term=?
        GROUP BY class, catalog_num
        ORDER BY class
        """,
        (term,),
    )
    conn.commit()

    return res.fetchall()
