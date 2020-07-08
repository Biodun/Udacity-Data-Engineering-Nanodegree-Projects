# Project 1: Data modeling with Postgres

![Sparkify logo](images/Sparkify_logo.png)

## Background
Our music streaming startup __Sparkify__ needs a data warehouse for analysing customer usage patterns. The goal is creating fact and dimension tables that will allow them to easily answer questions like:
* Who are the top 10 users by the number of songs listened to?
* What locales do most of customers live in?
* User distribution by geography and service tier (free vs paid)

In order to create the Data Warehouse, we need to create a Extract, Load and Transform (ETL) process for ingesting song play and log files. Samples of these two input file types are shown below:

#### Song files

```json
{
    "num_songs": 1,
    "artist_id": "ARD7TVE1187B99BFB1",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "California - LA",
    "artist_name": "Casual",
    "song_id": "SOMZWCG12A8C13C480",
    "title": "I Didn't Mean To",
    "duration": 218.93179,
    "year": 0
}
```

#### Log files

```json
{
    "artist": "Dee Dee Bridgewater",
    "auth": "Logged In",
    "firstName": "Lily",
    "gender": "F",
    "itemInSession": 38,
    "lastName": "Koch",
    "length": 318.64118,
    "level": "paid",
    "location": "Chicago-Naperville-Elgin, IL-IN-WI",
    "method": "PUT",
    "page": "NextSong",
    "registration": 1541048010796.0,
    "sessionId": 818,
    "song": "La Vie En Rose",
    "status": 200,
    "ts": 1542845032796,
    "userAgent": "\"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Ubuntu Chromium\/36.0.1985.125 Chrome\/36.0.1985.125 Safari\/537.36\"",
    "userId": "15"
}
```

## Data warehouse architecture and ETL Pipeline

We use a [Star schema](https://en.wikipedia.org/wiki/Star_schema) architecture with one fact table and four dimension tables, and our ETL pipeline consists of the following steps:
1. Use the `create_tables.py` script to create the _`sparkifydb`_ database which comprises of the following tables arranged in a :

    -  Fact table:
        - `songplays`
    - Dimension tables:
        - `users`
        - `songs`
        - `artists`
        - `time`    
2. Read and process data from the song data and log data files (stored in the `data\log_data`, and `data\song_data` folders), and load the processed data into the database using the `etl.py` script.

## Setup

1. Use [Docker](www.docker.com) to create a disposable Postgres container using the instructions in this great [blog article](https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198):

    * Navigate to [this](https://www.docker.com/get-started) webpage to install Docker if you don't already have it installed.
    * Create a Postgres database running on port 5432 in a Docker container 

        ```
        docker run --rm --name udacity-postgres-docker -d -e POSTGRES_PASSWORD=student -e POSTGRES_USER=student -e POSTGRES_DB=studentdb -p 5432:5432 postgres
        ```

2. Install the [Miniconda](https://docs.conda.io/en/latest/miniconda.html) package and environment manager to create an isolated python environment for this demo.
3. Clone this repo, then navigate to the `Projects/Data_modeling_with_Postgres` folder. Use the `environment.yml` file to create a conda environment with all the packages required to run the code in this repository:
> `conda env create --file environment.yml --name udacity_data_eng`

4. Activate the installed conda environment:
> `conda activate udacity_data_eng`

4. Navigate to `Projects/Data_modeling_with_Postgres` folder of this repository and  execute the following commands at command line:   
```
$ python src/create_tables.py
$ python src/etl.py
```
## Results
Use the following queries to explore the data we loaded into our database:

1. Query top 10 users by number of songs listened to:
```sql
SELECT COUNT(DISTINCT songplays.songplay_id) AS "Number of songs listened to", users.first_name, users.last_name 
FROM songplays JOIN users ON users.user_id = songplays.user_id
GROUP BY users.user_id
ORDER BY COUNT(DISTINCT songplay_id) DESC
LIMIT 10;
```
2. What locales do most of customers live in?

```sql
SELECT location, COUNT(DISTINCT user_id)
FROM songplays
GROUP BY location
ORDER BY COUNT(DISTINCT user_id) DESC
LIMIT 5; 
```

## To do
1. Add precommit hooks for code formatting and checking for secrets.
2. Create a [Streamlit tool](https://www.streamlit.io/) for visualizing the data


