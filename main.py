from core_logic import *

if __name__ == "__main__":
    print("Travel Agent Started")
    app.invoke({
        "destination": "Japan",
        "nationality": "American",
        "dates": "Dec 1st - Dec 15th, 2024",
        "purpose": "Tourism and sightseeing"
    })