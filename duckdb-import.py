import duckdb

con = duckdb.connect(':memory:')
con.install_extension('httpfs')
con.load_extension('httpfs')
# con.execute('SELECT * FROM duckdb_extensions();')


manifest_fname = 'fileurls.txt'
with open(manifest_fname, 'r') as f:
    urls = f.read().splitlines()
print(urls)


# Sample a few rows with all the columns of the dataset
con.execute(f'''
SELECT *
FROM parquet_scan({urls[0:1]})
LIMIT 5;
''')
sampledf = con.fetch_df()
print(sampledf)
print(sampledf.columns)
print()


# Count the number of taxi rides per year-month
con.execute(f'''
SELECT date_part('year', pickup_datetime) as pickup_year, date_part('month', pickup_datetime) as pickup_month, COUNT(*)
FROM parquet_scan({urls[0:]})
GROUP BY pickup_year, pickup_month
ORDER BY pickup_year, pickup_month;
''')
df = con.fetch_df()
print(df)
print(df.columns)
print()


# Create a view of the whole dataset
# (Basically just shortcut the query to 'nyc_taxi_tiny')
con.execute(f'''
CREATE VIEW nyc_taxi_tiny AS
SELECT *
FROM parquet_scan({urls});
''')


# Sample from that view
con.execute(f'''
SELECT *
FROM nyc_taxi_tiny
LIMIT 5;
''')
df = con.fetch_df()
print(df)
print(df.columns)
print()