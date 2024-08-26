# init_db.py

# Import required modules.
import sqlite3
import csv

# Create database connection and cursor object.
conn = sqlite3.connect("./data/database.db")
curs = conn.cursor()

# Drop the drones table if it exists.
curs.execute("DROP TABLE IF EXISTS drones;")

# Create a new drones table.
curs.execute(
    """
CREATE TABLE IF NOT EXISTS drones (
    id          INTEGER PRIMARY KEY,
    name        TEXT,
    flight_time INTEGER,
    sensor_size TEXT,
    weight      NUMERIC,
    top_speed   NUMERIC,
    cost        NUMERIC);
    """
)

# Open the CSV file for reading.
with open("drones.csv", "r") as csv_file:
    # Create a CSV reader object.
    csv_reader = csv.reader(csv_file)
    # Skip the header row.
    next(csv_reader)

    # Loop through each row in the CSV file.
    for row in csv_reader:
        # Convert the row to a tuple.
        drone_data = tuple(row)
        # Insert the drone data into the table.
        curs.execute(
            """
            INSERT INTO drones (name, flight_time, sensor_size, weight, top_speed, cost)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            drone_data,
        )

# Commit the changes and close the connection.
conn.commit()
conn.close()

