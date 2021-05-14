import pymysql
from sqlalchemy import create_engine

def sqlalc_conn():
    engine = create_engine("mysql+pymysql://jmawirat:cisco@10.66.69.144/service_discovery_nso_db")
    return engine