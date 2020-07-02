import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from psycopg2 import Error


def process_song_file(cur, filepath):
    """
    Parameters
    ----------
    cur: Postgres cursor
    filepath: str, filepath to song files
    
    Returns
    -------
    None
    """
    # open song file
    
    # TODO Add docstrings and error/exception handling
    
    # Parse the songfile
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    
    try:
        cur.execute(song_table_insert, song_data)
    except Error as e:
        print(f"ERROR!! The following error occurred while trying to insert song data into the database: {e}")
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0]

    # TODO Handle cases where the artist already exists in the database
    try:
        cur.execute(artist_table_insert, artist_data)
    except Error as e:
        print(f"ERROR!! The following error occurred while trying to insert artist data into the database: {e}\n{artist_data}")


def process_log_file(cur, filepath):
    """
    Parse log data files and ingest them into the database

    Parameters
    ----------
    cur: Postgres cursor
    filepath: str, filepath to song files
    
    Returns
    -------
    None
    """
    #TODO Add docstrings and error/exception handling

    # open log file and parse the timestamp column
    df = pd.read_json(filepath, lines=True, convert_dates=['ts'])

    # filter by NextSong action
    df = df.query("page=='NextSong'")
    
    # convert timestamp column to datetime
    time_data = [(f"{ts}", ts.hour, ts.day, ts.weekofyear, ts.month, ts.year, ts.weekday()) for ts in df['ts']]
    column_labels = ("timestamp", "hour", "day", "week", "month", "year", "weekday")
    
    # insert time data records
    time_df = pd.DataFrame(time_data, columns=column_labels)

    # TODO Ingest the entire dataframe at once rather than iterating through each row
    for i, row in time_df.iterrows():
        try:
            print(f"Inserting time data record {i+1} of {filepath} into the database")
            cur.execute(time_table_insert, list(row))
        except Error as e:
            print(f"ERROR!! The following error occurred while inserting time log data into the time table: {e}")

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # Drop any rows with duplicate userId's
    user_df = user_df.drop_duplicates(subset=["userId"])

    # TODO handle duplicate user entries into the users table 
    # insert user records
    for i, row in user_df.iterrows():
        try:
            print(f"Inserting user data record {i+1} of {filepath} into the database")
            cur.execute(user_table_insert, row)
        except Error as e:
            print(f"ERROR!! The following error occurred while inserting user data into the users table: {e}\n\n")
            raise ValueError

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        try:
            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fetchone()
        
            if results:
                songid, artistid = results
            else:
                songid, artistid = None, None

            # insert songplay record
            songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
            cur.execute(songplay_table_insert, songplay_data)
        
        except Error as e:
            print(f"ERROR! The following error occurred while retrieving song data for {row.userId} {row.song}, {row.artist}, {row.length}: {e}")

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        print(f"Processing {datafile}")
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.\n'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    print("Processing song data files....") 
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    print("Song data ingest completed.")
    print("Processing log data files....") 
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    print("Log data ingest completed.")
    conn.close()


if __name__ == "__main__":
    main()