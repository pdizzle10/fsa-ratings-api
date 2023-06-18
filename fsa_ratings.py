import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import requests
import os

os.mkdir("graphs")
os.chdir("graphs")

#get data from API and create DataFrame
url = "https://ratings.food.gov.uk/search/%5E/leeds/1/10000/json"
r = requests.get(url)
df = pd.DataFrame.from_dict(r.json()["FHRSEstablishment"]["EstablishmentCollection"]['EstablishmentDetail'])

#clean DataFrame by removing businesses that have not been given a rating and converting the Scores column from a Dictionary into 3 separate columns
df = df[(df["RatingValue"] != "AwaitingInspection") & (df["RatingValue"] != "Exempt") & (df["RatingValue"] != "Pass") & (df["LocalAuthorityName"] == "Leeds")]
df = pd.concat([df.drop("Scores", axis=1), df["Scores"].apply(pd.Series)], axis=1)

#turn the ratings columns to integers
df["Hygiene"] = pd.to_numeric(df["Hygiene"])
df["Structural"] = pd.to_numeric(df["Structural"])
df["ConfidenceInManagement"] = pd.to_numeric(df["ConfidenceInManagement"])

#create a second dataframe to be used specifically for the bar chart which aggregates and displays averages for each of the ratings. convert this to an easy to use format for seaborn
bars = round(df.groupby("BusinessType", as_index=False)[["BusinessType","Hygiene","Structural","ConfidenceInManagement"]].mean(),1)
bars = bars.melt("BusinessType", var_name="ratings", value_name="values")

#first chart plotting average food safety ratings by business type
sns.set(context="notebook")
sns.set_style("dark")
sns.barplot(data=bars, y="BusinessType", x="values", hue="ratings", color="c").set(ylabel = "Business Type",
                                                                        xlabel="Average rating")
plt.title('Average Food Safety ratings for businesses in Leeds', weight='bold').set_fontsize('24')
plt.legend(title="Food Safety Ratings")
plt.savefig("Average Food Safety Ratings.png")
plt.clf()


#second group of charts counting scores across the ratings categories 
ratings = ["Hygiene","Structural","ConfidenceInManagement"]

for rating in ratings:
    sns.countplot(data=df, x=df[rating], color="c", hue="BusinessType", palette="dark").set(ylabel = "Number of businesses",
                                                                                        xlabel = "Score")
    plt.title("How different businesses scored on the " + rating + " Food Safety rating", weight='bold').set_fontsize('24')
    plt.legend(title="Business Type")
    plt.savefig("Count of " + rating + " Food Safety rating.png")
    plt.clf()
