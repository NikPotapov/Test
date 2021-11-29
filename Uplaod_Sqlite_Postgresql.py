import sqlite3
import pandas as pd
from sqlalchemy import create_engine, exc


#configure credentials for engine
engine = create_engine('postgresql://postgres:(password)@(Name):(Port)/(Name db)')
con = sqlite3.connect('database.sqlite')

print("************ StateNames Data Processing ************")
# Check if the StateNames table exists, in case not create one
try:
    cur = engine.execute('SELECT 1 from "StateNames";')
except exc.SQLAlchemyError:
    print('StateNames table does not exist, starting to build...')
    cur = engine.execute('CREATE TABLE "StateNames" ("Id" serial PRIMARY KEY NOT NULL,'
                         ' "Name" VARCHAR (50) NOT NULL,'
                         ' "Year" Integer  NOT NULL,'
                         ' "Gender" VARCHAR (1) NOT NULL,'
                         ' "State" VARCHAR (2) NOT NULL,'
                         ' "Count" Integer NOT NULL);'
                         ' CREATE UNIQUE INDEX "indexes_state" '
                         'on "StateNames" ("Id", "Name", "Year", "Gender", "State", "Count");'
                         )
    print('Table - StateNames is created')

# Get data from Sqlite StateNames then upload into PostgreSQL to StateNames Table
max_id_State = str(pd.read_sql_query('SELECT Case When Max("Id") > 0 Then Max("Id") ELSE 0 END as "max" from '
                                     '"StateNames";', engine).at[0, 'max'])
df = pd.read_sql_query('Select * from StateNames Where id > ' + max_id_State + ';', con)
print('Uploading data to PostgreSQL db table - StateNames...')
df.to_sql('StateNames', con=engine, if_exists='append', index=False)
print('Done! Uploaded number of rows, columns: {}'.format(df.shape))
print('\n' * 2)

print("************ NationalNames Data Processing ************")
# Check if the NationalNames table exists, in case not create one
try:
    cur = engine.execute('SELECT 1 from "NationalNames";')
except exc.SQLAlchemyError:
    print('NationalNames table does not exist, starting to build...')
    cur = engine.execute('CREATE TABLE "NationalNames" ("Id" serial PRIMARY KEY NOT NULL,'
                         ' "Name" VARCHAR (50) NOT NULL,'
                         ' "Year" Integer NOT NULL,'
                         ' "Gender" VARCHAR (1) NOT NULL,'
                         ' "Count" Integer NOT NULL);'
                         ' CREATE UNIQUE INDEX "indexes_National" '
                         'on "NationalNames" ("Id", "Name", "Year", "Gender", "Count");'
                         )
    print('Table - NationalNames is created')

# Get data from Sqlite NationalNames then upload into PostgreSQL to NationalNames Table
max_id_National = str(pd.read_sql_query('SELECT Case When Max("Id") > 0 Then Max("Id") ELSE 0 END as "max" from '
                                        '"NationalNames";', engine).at[0, 'max'])
df = pd.read_sql_query('Select * from NationalNames Where id > ' + max_id_National + ';', con)
print('Uploading data to PostgreSQL db table - NationalNames...')
df.to_sql('NationalNames', con=engine, if_exists='append', index=False)
print('Done! Uploaded number of rows, columns: {}'.format(df.shape))