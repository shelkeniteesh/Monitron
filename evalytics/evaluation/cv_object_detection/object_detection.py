from evalytics.evaluation.service import ModelEvaluationService


class ObjectDetectionEvaluationService(ModelEvaluationService):
    def __init__(self):
        super().__init__()
        self.model_metrics.extend([
        ])

    def build_current_dataset(self, current_data_df, target_column: str | None = None, prediction_column: str | None = None):
        pass

    def build_reference_dataset(self, current_data_df, reference_data_df):
        pass