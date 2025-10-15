import random

import pandas as pd
from evidently import Report, DataDefinition, Dataset, MulticlassClassification, BinaryClassification
from evidently.presets import ClassificationPreset

# from .evaluation.service import ModelEvaluationService

# Sample data
# current = {
#     "name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Helen", "Ian", "Julia"],
#     "age": [25, 30, 35, 28, 22, 40, 33, 27, 31, 29],
#     "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
#              "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
#     "spam_prediction": [random.choice(["Yes", "No"]) for _ in range(10)],
#     "spam_groundtruth": [random.choice(["Yes", "No"]) for _ in range(10)],
# }
#
# reference = {
#     "name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Helen", "Ian", "Julia"],
#     "age": [25, 30, 35, 28, 22, 40, 33, 27, 31, 29],
#     "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
#              "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
#     "spam": [random.choice(["Yes", "No"]) for _ in range(10)]
# }
#
# current = pd.DataFrame({
#     "spam_groundtruth": ["Yes", "No", "Yes", "No", "Yes"],
#     "spam_prediction_probability": [0.92, 0.10, 0.78, 0.15, 0.60]
# })

# Create DataFrame
# current_df = pd.DataFrame(current)
# reference_df = pd.DataFrame(reference)
#
# current_data = Dataset.from_pandas(
#     data=current_df,
#     data_definition=DataDefinition(
#         classification=[BinaryClassification(
#             target="spam_groundtruth",
#             prediction_probas="spam_prediction_probability",
#             # prediction_labels="spam_prediction",
#             pos_label="Yes"
#         )]
#     )
# )
multiclass_df = pd.DataFrame({
    "true_label": ["Dog", "Cat", "Rabbit", "Dog", "Cat"],
    "predicted_label": ["Dog", "Rabbit", "Rabbit", "Cat", "Cat"],
    "Cat": [0.10, 0.10, 0.10, 0.70, 0.85],
    "Dog": [0.85, 0.20, 0.20, 0.10, 0.10],
    "Rabbit": [0.05, 0.70, 0.70, 0.20, 0.05]
})
current_data = Dataset.from_pandas(
    data=multiclass_df,
    data_definition=DataDefinition(
        classification=[MulticlassClassification(
            target="true_label",
            prediction_labels="predicted_label",
            prediction_probas=[ "Dog",  "Cat", "Rabbit" ]
        )
        ]
    )
)

report = Report([ClassificationPreset()])
print(report.run(current_data=current_data).dict())
