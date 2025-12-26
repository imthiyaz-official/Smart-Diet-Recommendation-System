from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# -------- Request Model --------
class PredictRequest(BaseModel):
    nutrition_input: List[int]
    ingredients: List[str]
    params: dict


# -------- API --------
@app.get("/")
def health_check():
    return {"health_check": "OK"}


@app.post("/predict")
def predict(data: PredictRequest):
    # Dummy recommendations (safe format)
    recipes = [
        {
            "Name": "Grilled Chicken Bowl",
            "Calories": 350,
            "Protein": 40,
            "Carbs": 20,
            "Fat": 10
        },
        {
            "Name": "Vegetable Omelette",
            "Calories": 280,
            "Protein": 25,
            "Carbs": 10,
            "Fat": 15
        },
        {
            "Name": "Rice & Broccoli",
            "Calories": 300,
            "Protein": 12,
            "Carbs": 50,
            "Fat": 5
        },
        {
            "Name": "Quinoa Salad",
            "Calories": 250,
            "Protein": 8,
            "Carbs": 40,
            "Fat": 8
        },
        {
            "Name": "Tofu Stir-fry",
            "Calories": 400,
            "Protein": 30,
            "Carbs": 30,
            "Fat": 12
        },
        {
        
            "Name": "Lentil Soup",
            "Calories": 220,
            "Protein": 18,
            "Carbs": 35,
            "Fat": 4
        },
        {
            "Name": "Greek Yogurt Parfait",
            "Calories": 200,
            "Protein": 15,
            "Carbs": 25,
            "Fat": 2
        },
        {
            "Name": "Salmon with Asparagus",
            "Calories": 450,
            "Protein": 35,
            "Carbs": 15,
            "Fat": 20
        },
        {
            "Name": "Turkey Wrap",
            "Calories": 320,
            "Protein": 28,
            "Carbs": 30,
            "Fat": 8
        },
        {
            "Name": "Chickpea Curry",
            "Calories": 380,
            "Protein": 22,
            "Carbs": 45,
            "Fat": 10
        },
        {
            "Name": "Vegetable Stir-fry",
            "Calories": 280,
            "Protein": 10,
            "Carbs": 35,
            "Fat": 12
        }
    ]
    return {"output": recipes}
# ================= TEST RUN (OPTIONAL) =================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)   
# To run the FastAPI app, execute this file directly.
