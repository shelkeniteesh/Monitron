from django.db import models
from django.contrib.auth.models import User

from ingestion.models import Model, Batch


# Create your models here.
class Metric(models.Model):
    id = models.AutoField(primary_key=True)
    metric_name = models.CharField(max_length=255)
    metric_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metrics_modified')
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)

class ModelMetric(models.Model):
    id = models.AutoField(primary_key=True)
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE)
    metric_id = models.ForeignKey(Metric, on_delete=models.CASCADE)
    threshold = models.JSONField() # For ByLabel Metrics
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_metrics_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_metrics_modified')
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)

class ModelMetricValue(models.Model):
    id = models.AutoField(primary_key=True)
    model_metric_id = models.ForeignKey(ModelMetric, on_delete=models.CASCADE)
    value = models.JSONField() # For ByLabel Metrics
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_metric_values_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_metric_values_modified')
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    process_date = models.DateTimeField()
