from pymongo import MongoClient
import pandas as pd

# Setting up MongoDB

client = MongoClient('localhost', 27017)
db = client.grailed_data




