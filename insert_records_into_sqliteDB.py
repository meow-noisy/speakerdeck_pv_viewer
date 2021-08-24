from pathlib import Path
import csv

import sqlite3

this_file_dir = Path(__file__).parent.resolve()

sqlitedb_path = this_file_dir / "db.sqlite3"
conn = sqlite3.connect(str(sqlitedb_path))
cur = conn.cursor()

# crate table
cur = conn.cursor()
table_name = 'slide'
cur.execute(f"DROP TABLE IF EXISTS {table_name}")

cur.execute(f"""CREATE TABLE {table_name}(
    slide_id TEXT UNIQUE NOT NULL,
    slide_title TEXT INTEGER NOT NULL,
    PRIMARY KEY (slide_id)
)""")
conn.commit()


# crate table
cur = conn.cursor()
table_name = 'slide_pv_date'
cur.execute(f"DROP TABLE IF EXISTS {table_name}")

cur.execute(f"""CREATE TABLE {table_name}(
    id INTEGER PRIMARY KEY,
    slide_id TEXT NOT NULL,
    pv INTEGER NOT NULL,
    date CHAR(10),
    FOREIGN KEY(slide_id) REFERENCES slide(slide_id),
    UNIQUE (slide_id, date)
)""")
conn.commit()


tsv_result_dir = this_file_dir / "result"

# 一番新しいtsvを取得(すべてのスライドを収集するため。)
l = sorted(list(tsv_result_dir.iterdir()), key=lambda x: str(x))
latest_csv_file = l[-1]

with latest_csv_file.open('r') as f:
    records = list(csv.reader(f, delimiter='\t'))


for slide_id, slide_title, _ in records:
    try:
        cur.execute(f'INSERT INTO slide (slide_id , slide_title) VALUES (?,?)',
                    (slide_id, slide_title))
        conn.commit()
    # 既に登録されていたら
    except sqlite3.IntegrityError:
        pass

for date_records in l:
    print(date_records)
    date = date_records.stem
    with date_records.open('r') as f:
        records = list(csv.reader(f, delimiter='\t'))
        for slide_id, slide_title, pv in records:
            try:
                cur.execute(
                    f'INSERT INTO slide_pv_date (slide_id , pv, date) VALUES (?,?,?)', (slide_id, pv, date))
            except sqlite3.IntegrityError:
                pass

conn.commit()
