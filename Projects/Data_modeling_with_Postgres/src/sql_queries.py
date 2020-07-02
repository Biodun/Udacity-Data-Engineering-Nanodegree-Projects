# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = (""" CREATE TABLE songplays (songplay_id SERIAL PRIMARY KEY, start_time TIMESTAMP, user_id VARCHAR(80), level VARCHAR(10), song_id VARCHAR(80), artist_id VARCHAR(80), session_id INTEGER, location TEXT, user_agent TEXT);
""")

user_table_create = (""" CREATE TABLE users (user_id VARCHAR(80) PRIMARY KEY, first_name VARCHAR(80), last_name VARCHAR(80), gender CHAR(1), level VARCHAR(10));
""")

song_table_create = (""" CREATE TABLE songs (song_id VARCHAR(80) PRIMARY KEY, title VARCHAR(80), artist_id VARCHAR(80), year SMALLINT, duration REAL);
""")

artist_table_create = (""" CREATE TABLE artists (artist_id VARCHAR(80) PRIMARY KEY, name TEXT, location VARCHAR(80), latitude REAL, longitude REAL);
""")

time_table_create = (""" CREATE TABLE time (start_time TIMESTAMP, hour SMALLINT, day VARCHAR(6), week SMALLINT, month SMALLINT, year SMALLINT,  weekday SMALLINT);
""")

# INSERT RECORDS

songplay_table_insert = (""" INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

# Do nothing if the user id already exists in the table
user_table_insert = (""" INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO NOTHING
""")

song_table_insert = (""" INSERT INTO songs (song_id, title,  artist_id, year, duration) VALUES (%s, %s, %s, %s, %s);
""")

# Do nothing if the artist entry already exists
artist_table_insert = (""" INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = (""" INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = (""" SELECT songs.song_id, artists.artist_id FROM songs JOIN artists ON artists.artist_id = songs.artist_id
WHERE songs.title = %s
AND artists.name = %s
AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]