from abc import ABC

from evidently import Report, Recsys, Dataset, DataDefinition
from evidently.presets import DataDriftPreset

from evalytics.exceptions import MissingDataMetricsDataException


class ModelEvaluationService(ABC):
    def __init__(self):
        self.model_metrics: list = []
        self.data_metrics: list = [
            DataDriftPreset(),
        ]
        self.mm_current_data=None,
        self.dm_current_data=None,
        self.dm_reference_data=None

    def evaluate(self):
        dm_metrics = dict()
        mm_metrics = dict()
        if self.mm_current_data:
            mm_metrics = self.evaluate_model_metrics(self.mm_current_data)
        if (self.dm_current_data and not self.dm_reference_data) or (not self.dm_current_data and self.dm_reference_data):
            raise MissingDataMetricsDataException()
        if self.dm_current_data and self.dm_reference_data:
            dm_metrics = self.evaluate_data_metrics(self.dm_current_data, self.dm_reference_data)

        mm_metrics_dict = {}
        dm_metrics_dict = {}
        if mm_metrics:
            mm_metrics_dict = {metric['metric_id'].split('(')[0].strip().lower(): metric['value'] for metric in mm_metrics['metrics']}
        if dm_metrics:
            dm_metrics_dict = {metric['metric_id'].split('(')[0].strip().lower(): metric['value'] for metric in dm_metrics['metrics']}

        return mm_metrics_dict | dm_metrics_dict

    def evaluate_model_metrics(self, mm_current_data):
        try:
            report = Report(metrics=self.model_metrics)
            return report.run(current_data=mm_current_data).dict()
        except Exception as e:
            raise RuntimeError(f"Error calculating model metrics: {e}")

    def evaluate_data_metrics(self, dm_current_data, dm_reference_data):
        try:
            report = Report(metrics=self.model_metrics)
            return report.run(current_data=dm_current_data, reference_data=dm_reference_data).dict()
        except Exception as e:
            raise RuntimeError(f"Error calculating data metrics: {e}")

    def build_reference_dataset(self, current_data_df, reference_data_df, numerical_columns: list[str] | None = None, categorical_columns: list[str] | None = None, text_columns: list[str] | None = None, datetime_columns: list[str] | None = None, numerical_descriptors: list[str] | None = None, categorical_descriptors: list[str] | None = None, test_descriptors: list[str] | None = None, ranking: list[Recsys] | None = None):
        self.dm_current_data = Dataset.from_pandas(
            data=current_data_df,
            data_definition=DataDefinition(
                numerical_columns=numerical_columns,
                categorical_columns=categorical_columns,
                text_columns=text_columns,
                datetime_columns=datetime_columns,
                numerical_descriptors=numerical_descriptors,
                categorical_descriptors=categorical_descriptors,
                test_descriptors=test_descriptors,
                ranking=ranking
            )
        )

        self.dm_reference_data = Dataset.from_pandas(
            data=reference_data_df,
            data_definition=DataDefinition(
                numerical_columns=numerical_columns,
                categorical_columns=categorical_columns,
                text_columns=text_columns,
                datetime_columns=datetime_columns,
                numerical_descriptors=numerical_descriptors,
                categorical_descriptors=categorical_descriptors,
                test_descriptors=test_descriptors,
                ranking=ranking
            )
        )