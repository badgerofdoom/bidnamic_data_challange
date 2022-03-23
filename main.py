from src.database import Database
import pandas as pd
from src.datawarehousescript import CREATE_TABLES, CREATE_VIEWS

print('connectin to database')
# create db connection
username: str = 'tester'
password: str = 'tester'
db = Database('Test_db', 'localhost', 5432)
db.connect(username, password)

# load csvs
print('load in data form CSV files')
# campaign_id,structure_value,status
campaigns = pd.read_csv('data/campaigns.csv')
# date,ad_group_id,campaign_id,clicks,cost,conversion_value,conversions,search_term
search_terms = pd.read_csv('data/search_terms.csv')
# ad_group_id,campaign_id,alias,status
adgroups = pd.read_csv('data/adgroups.csv')


# process add groups
print('processs ad groups data')
adgroups[['_shift', '_shopping', 'country', '_campaign_structure_value',
          'priority', '_random_string', '_hash']] = adgroups['alias'].str.split(" - ", expand=True)
engine = db.create_db_enigine(username, password)

print('insert processed ad-group data into database')
adgroups.to_sql(
    'adgroups', engine, method='multi', if_exists='replace')
print('insert campaign data into database')
campaigns.to_sql('campaigns', engine, method='multi', if_exists='replace')
print('insert search terms data into database')
search_terms.to_sql('search_terms', engine,
                    method='multi', if_exists='replace')


print('create reporting structure')
print('Create Datawarehouse Tables')
conn = db.connection

cur = conn.cursor()


cur.execute(CREATE_TABLES)

conn.commit()
print('Create Datawarehouse Views')
cur.execute(CREATE_VIEWS)

conn.commit()
print('datawarehouse created')
conn.close()
db.disconnect

print('Process Complete')
