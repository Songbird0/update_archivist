from django.db import models


class RemovedFile(models.Model):
    relative_path = models.CharField(max_length=255)

    def __str__(self):
        return "relative_path={}".format(self.relative_path)


class AddedFile(models.Model):
    relative_path = models.CharField(max_length=255)

    def __str__(self):
        return "relative_path={0}".format(self.relative_path)


class ModifiedFile(models.Model):
    relative_path = models.CharField(max_length=255)
    checksum = models.TextField()

    def __str__(self):
        return "relative_path={0}, sum={1}".format(self.relative_path, self.checksum)

class UnmodifiedFile(models.Model):
    relative_path = models.CharField(max_length=255)
    checksum = models.TextField()

    def __str__(self):
        return "relative_path={0}, sum={1}".format(self.relative_path, self.checksum)

class ScaffoldingState(models.Model):
    project_name = models.CharField(max_length=200)
    zipped_scaffolding_sum = models.TextField()
    """Represents the (compressed) scaffolding sum.
    
    Once uncompressed, the archivist will store the last blake2b sum to compare 
    to the next zip sum."""
