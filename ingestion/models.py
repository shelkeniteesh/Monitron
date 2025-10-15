from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


# Create your models here.
class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='batches_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='batches_modified')

class ModelType(models.Model):
    id = models.AutoField(primary_key=True)
    model_type = models.CharField(max_length=255)
    description = models.TextField()
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_types_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='model_types_modified')

class Model(models.Model):
    id = models.AutoField(primary_key=True)
    model_type_id = models.ForeignKey(ModelType, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=255)
    model_version = models.CharField(max_length=255)
    model_description = models.TextField()
    is_active = models.BooleanField(default=True)
    owner_email = models.EmailField()
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='models_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='models_modified')

class DatasetDescription(models.Model):
    id = models.AutoField(primary_key=True)
    model_id = models.ForeignKey(Model, on_delete=CASCADE)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dataset_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets_modified')

class DatasetColumn(models.Model):
    id = models.AutoField(primary_key=True)
    dataset_description_id = models.ForeignKey(DatasetDescription, on_delete=CASCADE)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dataset_columns_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dataset_columns_modified')

class IngestionTemplate:
    id = models.AutoField(primary_key=True)
    model_id = models.ForeignKey(Model, on_delete=CASCADE)
    dataset_id = models.ForeignKey(DatasetDescription, on_delete=CASCADE)
    process_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingestion_templates_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ingestion_templates_modified')

class DatasetRow(models.Model):
    id = models.AutoField(primary_key=True)
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE)
    dataset_id = models.ForeignKey(DatasetDescription, on_delete=models.CASCADE)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_modified')
    column_name = models.CharField(max_length=255)
    column_datatype = models.CharField(max_length=255)
    column_value = models.CharField(max_length=255)
    hash = models.IntegerField()
    class Meta:
        abstract = True

class GroundTruthDatasetRow(DatasetRow):
    pass

class InferenceDatasetRow(DatasetRow):
    pass

class TrainingDatasetRow(DatasetRow):
    pass