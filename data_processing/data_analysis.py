import pandas as pd
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.metrics import classification_report, accuracy_score

def summationofprices(category):
    prices = listings_df[listings_df['predicted_category'] == category]['price']
    newprices = listings_df[listings_df['predicted_category'] == category]['newprice']

    #using fillna to fill empty spaces of prices with newprices
    combinedprices = prices.fillna(newprices)
    combinedprices = combinedprices.astype(str).str.replace("$", "", regex=False)  #remove dollar sign

    #convert cleaned prices to float
    combinedprices = combinedprices.astype(float)

    #returning the sum and the number of rows for the number of elements
    return combinedprices.sum(), combinedprices.shape[0]

try:
    uri = "mongodb://localhost:27017"
    client = MongoClient(uri)

    database = client["grailed_data"]
    collection = database["data"]
    training_collection = database["category_training_data"]

    #retrival code in here
    returnedData = list(collection.find({}, {"Name": 1, "Price": 1, "NewPrice": 1, "OldPrice": 1, "Size": 1}))
    training_data = list(training_collection.find({}, {"name": 1, "category": 1}))  # Retrieves all documents with name and category

    #create DataFrame from returnedData with correct field names
    listings_df = pd.DataFrame(returnedData)

    #replace empty strings with NaN
    listings_df.replace("", np.nan, inplace=True)

    #rename columns to lowercase for consistency
    listings_df.rename(columns={
        "Name": "name",
        "Price": "price",
        "NewPrice": "newprice",
        "OldPrice": "oldprice",
        "Size": "size"
    }, inplace=True)

    # Extract names and categories from training_data and create DataFrame
    training_name = [doc['name'] for doc in training_data]
    training_category = [doc['category'] for doc in training_data]

    # Create DataFrame with both lists
    trainingdata_df = pd.DataFrame({
        'name': training_name,
        'category': training_category
    })

    #end retrival code here

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

#training data to categorize data
#begin analysis for name/categories

#cleaning data by converting to all lowercase and removing any non relevant characters
trainingdata_df['name'] = (
    trainingdata_df['name']
    .str.lower()
    .str.replace(r'[^a-z0-9\s]', '', regex=True)
)
listings_df['name'] = (
    listings_df['name']
    .str.lower()
    .str.replace(r'[^a-z0-9\s]', '', regex=True)
)

#TfidfVectorizer to transform listing_name into numerical features, removing unimportant terms
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
x_train = vectorizer.fit_transform(trainingdata_df['name']) #using training data 'name' as the x train
y_train = trainingdata_df['category'] #labels are not numeric, scikit-learn will automatically encode

#random forest classifer
model = RandomForestClassifier()
model.fit(x_train, y_train)

#transform listing name to match format for prediction
X_test = vectorizer.transform(listings_df['name'])

#predict categories for listingname_df
y_pred = model.predict(X_test)
listings_df['predicted_category'] = y_pred

#insertting predicted categories into the actual mongodb database
for index, row in listings_df.iterrows():

    #using _id as the unique identifier for each document
    filter_criteria = {"_id": row['_id']}

    #update operation
    update_operation = {"$set": {"predicted_category": row['predicted_category']}}

    #updating document in mongodb
    collection.update_one(filter_criteria, update_operation)

print("predicted_category have been updated in the mongodb collection.")
client.close()

html_string = listings_df.to_html(index=False)  # Convert DataFrame to HTML, without index column

# Save to HTML file
with open('dataframe.html', 'w') as file:
    file.write(html_string)

print("DataFrame exported to 'dataframe.html'")

#calculating statistics for various stats such as average price

totalprice, numelements = summationofprices('tops')

print("listingsprices exported to 'listingsprices.html'")
print("The average price of bottoms is:", totalprice/numelements, " dollars!")