import sqlite3
import time
import random

def create_table(cursor: sqlite3.Cursor):
    cursor.execute('''
                   CREATE TABLE stats(
                       TIMESTAMP INTEGER,
                       ODOM_X REAL,
                       ODOM_Y REAL,
                       ODOM_Z REAL,
                       LEFT_VEL_1 REAL,
                       LEFT_VEL_2 REAL,
                       LEFT_VEL_3 REAL,
                       RIGHT_VEL_1 REAL,
                       RIGHT_VEL_2 REAL,
                       RIGHT_VEL_3 REAL
                   );''')

def insert_random(cursor: sqlite3.Cursor):
    cursor.execute('''
                   INSERT INTO stats (TIMESTAMP, ODOM_X, ODOM_Y, ODOM_Z, LEFT_VEL_1, LEFT_VEL_2, LEFT_VEL_3, RIGHT_VEL_1, RIGHT_VEL_2, RIGHT_VEL_3)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (int(time.time()),
                    round(random.uniform(-200, 200), 1),
                    round(random.uniform(-200, 200), 1),
                    round(random.uniform(-200, 200), 1),
                    round(random.uniform(-200, 200), 1),
                    round(random.uniform(-200, 200), 1),
                    round(random.uniform(-200, 200), 1),
                    round(random.uniform(-200, 200), 1),
                    round(random.uniform(-200, 200), 1),
                    round(random.uniform(-200, 200), 1)))
    cursor.connection.commit()

def benchmark_inserts(cursor: sqlite3.Cursor):
    start_time = time.time()
    end_time = start_time + 60  # Run for 10 seconds
    count = 0
    total_delta_time = 0
    last_time = time.time()

    while time.time() < end_time:
        insert_random(cursor)
        current_time = time.time()
        total_delta_time += (current_time - last_time)
        last_time = current_time
        count += 1

    average_delta_time = total_delta_time / count if count > 0 else 0
    print(f"Number of inserts in 10 seconds: {count}")
    print(f"Average delta: {average_delta_time:.6f} seconds")

def main():
    print("Hello from sqlite-python-benchmark!")
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        cursor.execute("select sqlite_version();")
        result = cursor.fetchall()
        print(result)
        print("\n\nBenchmarking sqlite3 inserts...\n\n")
        create_table(cursor)

        benchmark_inserts(cursor)

        result = cursor.execute('''SELECT * FROM stats;''') 
        print(f"Amount of rows in the table: {len(result.fetchall())}")


if __name__ == "__main__":
    main()
