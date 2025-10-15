from evidently import Dataset, DataDefinition, MulticlassClassification, BinaryClassification
from evidently.legacy.metric_preset import ClassificationPreset

from evalytics.evaluation.service import ModelEvaluationService


class BinaryClassificationEvaluationService(ModelEvaluationService):
    def __init__(self):
        super().__init__()
        self.model_metrics.extend([
            ClassificationPreset()
        ])

    def build_current_dataset(self, current_data_df, target_column: str | None = None, prediction_column: str | None = None, prediction_scores: list[str] | None = None):
        """
        Args:
            current_data_df : Pandas dataframe containing the current data.
            target_column (str, optional): The name of the column containing the true class labels (e.g., "true_label").
            prediction_column (str, optional): The name of the column containing the predicted class labels (e.g., "predicted_label").
            prediction_scores (str, optional): The name of the column containing the predicted probability for the positive class
                (e.g., "spam_prediction_probability"). This should be a single probability score between 0 and 1.                These column names should correspond to the class labels themselves (e.g., ["Dog", "Cat", "Rabbit"]).
            Either prediction_column can be specified if prediction as distinct label, if not prediction scores should be specified.
        Returns:
            Dataset: An 'Evidently' Dataset object with the appropriate binary classification schema.

        Raises:
            ValueError: If any of the required arguments are missing or inconsistent with the DataFrame schema.
        """
        self.mm_current_data = Dataset.from_pandas(
            data=current_data_df,
            data_definition=DataDefinition(
                classification=[BinaryClassification(
                    target=target_column,
                    prediction_labels=prediction_column,
                    prediction_probas=prediction_scores
                )
                ]
            )
        )