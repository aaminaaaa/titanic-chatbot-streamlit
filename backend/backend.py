from fastapi import FastAPI, Query
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re

app = FastAPI()

# Load Titanic dataset
df = pd.read_csv("titanic.csv")

# Function to convert Matplotlib plots to base64-encoded images
def plot_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@app.get("/query")
def query_titanic(question: str = Query(..., title="User Query")):
    """Handles Titanic-related user queries dynamically."""
    question_lower = question.lower()
    response = "I can only answer Titanic-related data questions for now."
    image_base64 = None

    try:
        # Total passengers
        if re.search(r"(how many|total number of).*passengers", question_lower):
            total_passengers = len(df)
            response = f"There were {total_passengers} passengers on the Titanic."

        # Survival statistics
        elif re.search(r"(percentage|rate).*surviv(ed|ors)", question_lower):
            survived_pct = (df['Survived'] == 1).mean() * 100
            response = f"{survived_pct:.2f}% of passengers survived."

        elif re.search(r"(how many|number of).*surviv(ed|ors)", question_lower):
            survivors = df[df["Survived"] == 1].shape[0]
            response = f"{survivors} passengers survived."

        # Gender-based survival and distribution
        elif re.search(r"(how many|number of).*women.*surviv(ed|ors)", question_lower):
            women_survived = df[(df["Sex"] == "female") & (df["Survived"] == 1)].shape[0]
            response = f"{women_survived} women survived."

        elif re.search(r"(how many|number of).*men.*surviv(ed|ors)", question_lower):
            men_survived = df[(df["Sex"] == "male") & (df["Survived"] == 1)].shape[0]
            response = f"{men_survived} men survived."

        elif re.search(r"(what percentage).*male", question_lower):
            total_passengers = len(df)
            male_count = (df['Sex'] == 'male').sum()
            male_pct = (male_count / total_passengers) * 100
            response = f"{male_pct:.2f}% of passengers were male."

        elif re.search(r"(what percentage).*female", question_lower):
            total_passengers = len(df)
            female_count = (df['Sex'] == 'female').sum()
            female_pct = (female_count / total_passengers) * 100
            response = f"{female_pct:.2f}% of passengers were female."

        elif re.search(r"(percentage of females who survived)", question_lower):
            total_females = df[df["Sex"] == "female"].shape[0]
            female_survived = df[(df["Sex"] == "female") & (df["Survived"] == 1)].shape[0]
            female_survival_rate = (female_survived / total_females) * 100 if total_females > 0 else 0
            response = f"{female_survival_rate:.2f}% of female passengers survived."

        # Class-based survival
        elif re.search(r"(survival rate).*class (\d+)", question_lower):
            class_number = int(re.findall(r"\d+", question_lower)[0])
            survival_rate = df[df["Pclass"] == class_number]["Survived"].mean() * 100
            response = f"Survival rate for class {class_number}: {survival_rate:.2f}%"

        elif re.search(r"(how many passengers).*class (\d+)", question_lower):
            class_number = int(re.findall(r"\d+", question_lower)[0])
            class_count = df[df["Pclass"] == class_number].shape[0]
            response = f"There were {class_count} passengers in class {class_number}."

        # Age-related insights
        elif re.search(r"(average|mean).*age", question_lower):
            avg_age = df["Age"].mean()
            response = f"The average age of passengers was {avg_age:.2f} years."

        elif re.search(r"(histogram|distribution).*age", question_lower):
            fig, ax = plt.subplots()
            sns.histplot(df["Age"].dropna(), bins=20, kde=True, ax=ax)
            ax.set_title("Age Distribution of Titanic Passengers")
            image_base64 = plot_to_base64(fig)

        # Fare details
        elif re.search(r"(average|mean).*fare", question_lower):
            avg_fare = df["Fare"].mean()
            response = f"The average ticket fare was ${avg_fare:.2f}."

        elif re.search(r"(fare vs survival|correlation).*fare", question_lower):
            fig, ax = plt.subplots()
            sns.boxplot(x="Survived", y="Fare", data=df, ax=ax)
            ax.set_title("Fare vs. Survival")
            image_base64 = plot_to_base64(fig)

        # Passenger embarkation
        elif re.search(r"(how many|number of).*passengers.*embarked", question_lower):
            fig, ax = plt.subplots()
            sns.countplot(x=df["Embarked"].dropna(), ax=ax)
            ax.set_title("Passengers per Embarkation Port")
            image_base64 = plot_to_base64(fig)

        # Passenger class distribution
        elif re.search(r"(how many|number of).*passengers.*class", question_lower):
            class_counts = df["Pclass"].value_counts().to_dict()
            response = f"Passengers per class: {class_counts}"

        # Family relationships
        elif re.search(r"(how many|number of).*siblings", question_lower):
            avg_sibsp = df["SibSp"].mean()
            response = f"The average number of siblings/spouses per passenger was {avg_sibsp:.2f}."

        elif re.search(r"(how many|number of).*parents", question_lower):
            avg_parch = df["Parch"].mean()
            response = f"The average number of parents/children per passenger was {avg_parch:.2f}."

    except Exception as e:
        response = f"An error occurred: {str(e)}"

    return {"response": response, "image": image_base64}