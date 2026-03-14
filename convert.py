import csv
import sqlite3
import glob
import os

def convert():
    # 查找解压后的 CSV 文件
    csv_files = glob.glob("**/GeoLite2-City-Locations-en.csv", recursive=True)
    if not csv_files:
        print("未找到 CSV 文件")
        return
    
    csv_file = csv_files[0]
    # 生成 NetBird 要求的特定日期文件名
    db_file = "geonames_20251217.db"
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 根据 NetBird 源码，它可能需要这个特殊的表名
    # 如果 source.geonames 报错，尝试 CREATE TABLE geonames
    cursor.execute("DROP TABLE IF EXISTS geonames")
    cursor.execute("""
        CREATE TABLE geonames (
            geoname_id INTEGER PRIMARY KEY,
            locale_code TEXT,
            continent_code TEXT,
            continent_name TEXT,
            country_iso_code TEXT,
            country_name TEXT,
            subdivision_1_iso_code TEXT,
            subdivision_1_name TEXT,
            subdivision_2_iso_code TEXT,
            subdivision_2_name TEXT,
            city_name TEXT,
            metro_code TEXT,
            time_zone TEXT,
            is_in_european_union INTEGER
        )
    """)

    with open(csv_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        to_db = [
            (
                row['geoname_id'], row['locale_code'], row['continent_code'],
                row['continent_name'], row['country_iso_code'], row['country_name'],
                row['subdivision_1_iso_code'], row['subdivision_1_name'],
                row['subdivision_2_iso_code'], row['subdivision_2_name'],
                row['city_name'], row['metro_code'], row['time_zone'],
                1 if row['is_in_european_union'] == '1' else 0
            )
            for row in reader
        ]

    cursor.executemany("INSERT INTO geonames VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", to_db)
    conn.commit()
    conn.close()
    print(f"成功转换至 {db_file}")

if __name__ == "__main__":
    convert()
