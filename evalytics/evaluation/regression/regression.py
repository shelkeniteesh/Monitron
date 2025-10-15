from evidently import Dataset, DataDefinition, MulticlassClassification, BinaryClassification, Regression
from evidently.legacy.metric_preset import ClassificationPreset, RegressionPreset

from evalytics.evaluation.service import ModelEvaluationService


class RegressionEvaluationService(ModelEvaluationService):
    def __init__(self):
        super().__init__()
        self.model_metrics.extend([
            RegressionPreset()
        ])

    def build_current_dataset(self, current_data_df, target_column: str | None = None, prediction_column: str | None = None):
        """
        Args:
            current_data_df : Pandas dataframe containing the current data.
            target_column (str, optional): The name of the column containing the true value for the target (e.g., "target").
            prediction_column (str, optional): The name of the column containing the predicted value for the target (e.g., "prediction").
        Returns:
            Dataset: An 'Evidently' Dataset object with the appropriate regression schema.

        Raises:
            ValueError: If any of the required arguments are missing or inconsistent with the DataFrame schema.
        """
        self.mm_current_data = Dataset.from_pandas(
            data=current_data_df,
            data_definition=DataDefinition(
                regression=[Regression(
                    target=target_column,
                    prediction=prediction_column
                )
                ]
            )
        )