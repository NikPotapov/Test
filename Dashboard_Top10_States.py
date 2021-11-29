from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px

#configure credentials for engine
engine = create_engine('postgresql://postgres:(password)@(Name):(Port)/(Name db)')
df = pd.read_sql_query('Select "State" ,Sum("Count") as "Count" from  "StateNames" '
                       'Where "State" in (SELECT "State" from "StateNames" '
                       'Group by "State" Order by Sum("Count") desc Limit 10) '
                       'Group by "State" Order by "Count" asc;', engine)

fig = px.bar(df, x='Count', y='State',
             hover_data=['Count', 'State'], color='Count',
             labels={'State': 'State'}, height=800)


fig.update_layout(
    title={'text': 'Top 10 states in newborns'})


fig.show()
