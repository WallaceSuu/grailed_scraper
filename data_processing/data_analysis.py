import pandas as pd
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.model_selection import train_test_split
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
#split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    trainingdata_df['name'],
    trainingdata_df['category'],
    test_size=0.2,
    random_state=42
)

#fit the vectorizer on the training data only
X_train_vect = vectorizer.fit_transform(X_train)

#transform the test data using the same vectorizer
X_test_vect = vectorizer.transform(X_test)

#create and train the Random Forest classifier
model = RandomForestClassifier()
model.fit(X_train_vect, y_train)

#make predictions on the testing set
y_pred = model.predict(X_test_vect)

#evaluate the model using classification report
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

#predicting categories for listings_df using trained model above
X_listings_vect = vectorizer.transform(listings_df['name'])  # Use the same vectorizer for listings
y_pred_listings = model.predict(X_listings_vect)

#insert predicted categories into the actual MongoDB database
for index, row in listings_df.iterrows():
    #using _id as the unique identifier for each document
    filter_criteria = {"_id": row['_id']}
    update_operation = {"$set": {"predicted_category": y_pred_listings[index]}}

    #updating documents in MongoDB
    collection.update_one(filter_criteria, update_operation)

print("predicted_category have been updated in the MongoDB collection.")

#pulling predicted_category from mongodb
retrievedData = list(collection.find({}, {"_id": 1, "predicted_category": 1}))

#create a mapping from _id to predicted_category
predicted_mapping = {doc['_id']: doc['predicted_category'] for doc in retrievedData}

#update listings_df with the predicted_category
listings_df['predicted_category'] = listings_df['_id'].map(predicted_mapping)

#export to HTML file (for viewing purposes)
html_string = listings_df.to_html(index=False)  # Convert DataFrame to HTML, without index column

#save to HTML file
with open('dataframe.html', 'w') as file:
    file.write(html_string)

print("DataFrame exported to 'dataframe.html'")

#calculating statistics for various stats such as average price
inputcategory = "accessories"
totalprice, numelements = summationofprices(inputcategory)
print("The average price of", numelements, inputcategory, "is:", round(totalprice / numelements, 2), "dollars!")

client.close()