# Test
1) Develop a pipeline using some workflow management platform. The pipeline is monitored, and the process can be scheduled to run regularly.
- For that task we can build a job in CI tool like Jenkins for regularly run and monitoring (example shell command - sudo python3 -m folder.Upload_Sqlite_Postgresql, time to run is the second day every month between at 10-11 am  (H H(10-11) 2 * *))
2) You use a SQL database (for example, Postgres) as the data warehouse
- Implemented one pipeline which can get (sqlite3 database) data and insert into Postgresql.
Views(sql) should be built manually once (I think it is better for the future updating if the client will request to change).
3) Develop a dashboard to visualize insight
- Solution is to build visualization in PowerBI and at the same time I tried to customize it in Plotly Dash (It is my first experience in Plotly Dash).
