
from fastapi import FastAPI, Query
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Load the dataset
df = pd.read_csv("titanic.csv")
app = FastAPI()
def plot_to_base64(fig):
    """Converts matplotlib figure
     to a Base64 string."""
    buffer = BytesIO()
    fig.savefig(buffer, format="png",bbox_inches="tight")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")

@app.get("/query")
def query_titanic(question: str = Query(..., title="User Query")):
    """Handles user queries dynamically."""
    question_lower = question.lower()
    response = "I can only answer Titanic-related data questions for now."
    image_base64 = None
    
    try:
        if "percentage" in question_lower and "male" in question_lower:
             male_pct = (df['Sex'] == 'male').mean() * 100
             response = f"{male_pct:.2f}% of passengers were male."
        elif "percentage" in question_lower and "survived" in question_lower:
            survived_pct = (df['survived'] == 1).mean() * 100
            response = f"{survived_pct:.2f}% of passengers survived."
        elif "histogram" in question_lower and "age" in question_lower:
            fig, ax = plt.subplots()
            sns.histplot(df['Age'].dropna(), bins=20, kde=True, ax=ax)
            ax.set_title("Histogram of Passenger Ages")
            image_base64 = plot_to_base64(fig)
        elif "average" in question_lower and "fare" in question_lower:
            avg_fare = df['Fare'].mean()
            response = f"The average ticket fare was ${avg_fare:.2f}."
        elif "passengers" in question_lower and "embarked" in question_lower:
            fig, ax = plt.subplots()
            sns.countplot(x=df['Embarked'].dropna(), ax=ax)
            ax.set_title("Number of Passengers per Embarkation Port")
            image_base64 = plot_to_base64(fig)
        elif "passengers" in question_lower and "class" in question_lower:
            class_counts = df['Pclass'].value_counts().to_dict()
            response = f"Passengers per class: {class_counts}"
        elif "children" in question_lower and "survived" in question_lower:
            children_survived = df[(df["Age"] < 18) & (df["Survived"] == 1)].shape[0]
            response = f"{children_survived} children survived the Titanic disaster."
        elif "women" in question_lower and "survived" in question_lower:
            women_survived = df[(df["Sex"] == "female") & (df["Survived"] == 1)].shape[0]
            response = f"{women_survived} women survived the Titanic disaster."
        elif "correlation" in question_lower and "fare" in question_lower:
            fig, ax = plt.subplots()
            sns.boxplot(x="Survived", y="Fare", data=df, ax=ax)
            ax.set_title("Fare vs. Survival")
            image_base64 = plot_to_base64(fig)
    except Exception as e:
        response = f"An error occurred: {str(e)}"
    return {"response": response, "image": image_base64}