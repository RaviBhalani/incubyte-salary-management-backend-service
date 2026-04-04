from django.db import models


class Timestamps(models.Model):
    """
    Base model for timestamp fields
    """

    created_ts = models.DateTimeField(auto_now_add=True)
    modified_ts = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreatedBy(models.Model):
    """
    Base model for created_by field
    """

    created_by = models.ForeignKey(
        "user.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_created_by"
    )

    class Meta:
        abstract = True


class ModifiedBy(models.Model):
    """
    Base model for modified_by field
    """
    
    class Meta:
        abstract = True

    modified_by = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_modified_by")


class IsActive(models.Model):
    """ 
    Base model for is_active field
    """ 
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True)


