#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[6]:


import pandas as pd

# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = f'{prefix}/yellow_tripdata_2021-01.csv.gz'

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    url,
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)

df = pd.read_csv(url, nrows=1000)


# In[4]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[7]:


len(df)


# In[10]:


df_iter = pd.read_csv(
    url,
    nrows=600,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100
)


# In[11]:


first = True

from tqdm.auto import tqdm

for df_chunk in tqdm(df_iter):

    if first:
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        first = False
        print("Table created")

    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))


# In[ ]:





# In[ ]:




