import pandas as pd
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

try:
    uri = "mongodb://localhost:27017"
    client = MongoClient(uri)

    database = client["grailed_data"]
    collection = database["data"]
    training_collection = database["category_training_data"]

    #retrival code in here
    returnedData = collection.distinct("Name")
    training_data = list(training_collection.find({}, {"name": 1, "category": 1}))  # Retrieves all documents with name and category

    #create dataframes
    listingname_df = pd.DataFrame(returnedData, columns=["listing_name"])

    # Extract names and categories from training_data and create DataFrame
    training_name = [doc['name'] for doc in training_data]
    training_category = [doc['category'] for doc in training_data]

    # Create DataFrame with both lists
    trainingdata_df = pd.DataFrame({
        'name': training_name,
        'category': training_category
    })

    #end retrival code in here
    client.close()

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
listingname_df['listing_name'] = (
    listingname_df['listing_name']
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
X_test = vectorizer.transform(listingname_df['listing_name'])

#predict categories for listingname_df
y_pred = model.predict(X_test)
listingname_df['predicted_category'] = y_pred

html_string = listingname_df.to_html(index=False)  # Convert DataFrame to HTML, without index column

# Save to HTML file
with open('dataframe.html', 'w') as file:
    file.write(html_string)

print("DataFrame exported to 'dataframe.html'")
