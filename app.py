from flask import Flask, render_template, request
import pickle
import json
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load models
models = {
    "knn": pickle.load(open("models/knn.pkl", "rb")),
    "nb": pickle.load(open("models/NB.pkl", "rb"))
}

# Load performance files
performances = {
    "knn": json.load(open("performance/performance_k.json")),
    "nb": json.load(open("performance/performance_n.json"))
}


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    performance = None
    selected_model = None

    if request.method == "POST":
        try:
            selected_model = request.form["model"]
            model = models[selected_model]
            performance = performances[selected_model]

            sl = float(request.form["sepal_length"])
            sw = float(request.form["sepal_width"])
            pl = float(request.form["petal_length"])
            pw = float(request.form["petal_width"])

            features = pd.DataFrame(
                [[sl, sw, pl, pw]],
                columns=[
                    "SepalLengthCm",
                    "SepalWidthCm",
                    "PetalLengthCm",
                    "PetalWidthCm"
                ]
            )

            pred = model.predict(features)[0]

            species = ["Setosa", "Versicolor", "Virginica"]
            prediction = species[int(pred)]

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template(
        "index.html",
        prediction=prediction,
        performance=performance,
        selected_model=selected_model
    )


if __name__ == "__main__":
    app.run(debug=True)
