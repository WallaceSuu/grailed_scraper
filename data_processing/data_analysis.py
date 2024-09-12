from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split

# Setting up MongoDB
client = MongoClient('localhost', 27017)
db = client.grailed_data

#grabbing the csv file exported via mongoDB
df = pd.read_csv('../grailed_data.data.csv', encoding = "latin-1")
df = df.fillna(0)

#we need to filter the data so that the newest price will always be displayed if it exists
df['Price'] = df['NewPrice'].where(df['NewPrice'].notna(), df['Price']) 


#removing columns that won't be used, such as NewPrice and OldPrice after the previous operation is done (might need to change later)
X = df.drop(columns=['_id', 'Price', 'NewPrice', 'OldPrice', 'LastBump', 'Link'])
X.fillna(0) #filling all the NaN values

print(X)

# NEED TO PERFORM ONE-HOT ENCODING OR LABEL ENCODING
# THIS WILL CHANGE THE CATEGORIES OF "NAME", "SIZE", "TIME" TO NUMERICAL VALES THAT CAN BE USED IN MACHINE LEARNING



#y is the price as we are trying to predict the price based on the characters entered
y = df['Price']

#training inputs (x) and outputs(y)
#in this case, inputs would be size/name and output would be price
#X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=53, test_size:0.2)





