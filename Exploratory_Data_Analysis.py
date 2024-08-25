# Import necessary libraries for data manipulation and analysis
import pandas as pd
import numpy as np

# Import libraries for data visualization
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# Import library for sentiment analysis
from textblob import TextBlob

# Load the dataset into a pandas DataFrame
data = pd.read_csv("drugsCom_raw/drugsComTrain_raw.tsv", delimiter='\t')

# Display the first few rows of the dataset
data.head()

# Get the column names in the dataset
data.columns

# Check for missing values in the dataset
data.isnull().sum()

# Identify unique drug names in the dataset
unique_drugs = data['drugName'].unique().tolist()

# Count the number of unique drugs in the dataset
num_unique_drugs = len(unique_drugs)

# Identify the most commonly reviewed drugs
popular_drugs = data['drugName'].value_counts()

# Display the top 20 most commonly reviewed drugs
top_20_drugs = popular_drugs.nlargest(20)

# Plot the top 20 most commonly reviewed drugs
plt.figure(figsize=(20, 10))
top_20_drugs.plot(kind='bar')
plt.title("Top 20 Most Popular Drugs by Review Count")
plt.show()

# Identify the least commonly reviewed drugs
least_20_drugs = popular_drugs.nsmallest(20)

# Plot the least commonly reviewed drugs
plt.figure(figsize=(20, 10))
least_20_drugs.plot(kind='bar')
plt.title("Top 20 Least Popular Drugs by Review Count")
plt.show()

# Create a dictionary of common drug suffixes and their associated classifications
drug_suffixes = {
    "azole": "antifungal (except metronidazole)",
    "caine": "anesthetic",
    "cillin": "antibiotic (penicillins)",
    "mycin": "antibiotic",
    "micin": "antibiotic",
    "cycline": "antibiotic",
    "oxacin": "antibiotic",
    "ceph": "antibiotic (cephalosporins)",
    "cef": "antibiotic (cephalosporins)",
    "dine": "H2 blockers (anti-ulcers)",
    "done": "opioid analgesics",
    "ide": "oral hypoglycemics",
    "lam": "anti-anxiety",
    "pam": "anti-anxiety",
    "mide": "diuretics",
    "zide": "diuretics",
    "nium": "neuromuscular blocking agents",
    "olol": "beta blockers",
    "tidine": "H2 antagonist",
    "tropin": "pituitary hormone",
    "zosin": "alpha blocker",
    "ase": "thrombolytics",
    "plase": "thrombolytics",
    "azepam": "anti-anxiety (benzodiazepine)",
    "azine": "antipsychotics (phenothiazine)",
    "barbital": "barbiturate",
    "dipine": "calcium channel blocker",
    "lol": "beta blocker",
    "zolam": "CNS depressants",
    "pril": "ACE inhibitor",
    "sartan": "angiotensin II receptor antagonists",
    "statin": "HMG CoA inhibitors",
    "vir": "antiviral substances"
}

# Perform sentiment analysis on the reviews using TextBlob
data['sentiment'] = data['review'].apply(lambda review: TextBlob(review).sentiment.polarity)

# Calculate the average sentiment score across all reviews
average_sentiment = data['sentiment'].mean()

# Plot the distribution of sentiment scores
plt.figure(figsize=(10, 5))
data['sentiment'].plot(kind='hist', bins=50)
plt.title("Distribution of Sentiment Scores")
plt.show()

# Get summary statistics for the usefulCount column
useful_count_stats = data['usefulCount'].describe()

# Get summary statistics for the rating column
rating_stats = data['rating'].describe()

# Visualize the distribution of ratings
plt.figure(figsize=(20, 10))
sns.countplot(data['rating'])
plt.title("Distribution of Ratings")
plt.show()

# Visualize the relationship between ratings and useful counts
plt.figure(figsize=(20, 10))
sns.scatterplot(x='rating', y='usefulCount', data=data)
plt.title("Relationship Between Rating and Useful Count")
plt.show()

# Visualize the distribution of sentiment scores with a KDE plot
plt.figure(figsize=(20, 10))
sns.histplot(data['sentiment'], kde=True)
plt.title("Distribution of Sentiment Scores with KDE")
plt.show()

# Calculate and plot the average useful count per day
data.groupby('date')['usefulCount'].mean().plot(figsize=(20, 10))
plt.title("Average Useful Count Per Day Over Time")
plt.show()

# Calculate and plot the average sentiment score per day
data.groupby('date')['sentiment'].mean().plot(figsize=(20, 10))
plt.title("Average Sentiment Score Per Day Over Time")
plt.show()

# Calculate and plot the number of reviews per day
data.groupby('date')['review'].size().plot(figsize=(20, 10))
plt.title("Number of Reviews Per Day Over Time")
plt.show()

# Group data by date and calculate summary statistics for further analysis
grouped_by_date = data.groupby('date').agg({
    'rating': np.mean,
    'usefulCount': np.sum,
    'review': np.size
})
grouped_by_date.index = pd.DatetimeIndex(grouped_by_date.index)

# Plot the number of reviews for a specific month
grouped_by_date['2008-04'].plot()
plt.title("Number of Reviews for April 2008")
plt.show()

# Save the dataset with sentiment scores to a new CSV file
data.to_csv("drug_review_dataset_with_sentiment.csv", index=False)