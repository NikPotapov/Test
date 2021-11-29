from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)

#configure credentials for engine
engine = create_engine('postgresql://postgres:(password)@(Name):(Port)/(Name db)')
df = pd.read_sql_query('SELECT "Name", Sum("Count") as "Count" '
                       'From "StateNames" Group by "Name" '
                       'Order by Sum("Count") desc Limit 10;', engine)


df.sort_values(['Count'], ascending=False)
fig = px.bar(df, x='Name', y='Count')

fig.update_layout(
    title={'text': 'Top 10 Names'})
fig.show()