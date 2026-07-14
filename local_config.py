INSTITUTE_API_TOKEN = 'dtyIfKlxZSkk9zSC0YG0yCqATSSh0UIfcdiJ1yo4yFt7nqPknBgKugvTAprM'

INSTITUTE_SOLRQUERY_URL = 'https://api.adsabs.harvard.edu/v1/search/query'
INSTITUTE_OPENURL_DATA = '/proj/ads/abstracts/links/openurl_servers_bbb.txt'

SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://vault:fk49dl23jmfo3jmsi3sa@adsabs-psql-bg.ci1iae2ep00k.us-east-1.rds.amazonaws.com:5432/vault'

# added by eb-deploy (over-write config values) from environment
try:
    import os, json
    G = globals()
    for k, v in os.environ.items():
        if k == k.upper() and k in G:
            print('overwriting config', k, 'old val=', G[k], 'new val=', v)
            try:
                w = json.loads(v)
                G[k] = w
            except:
                G[k] = v
except:
    pass
