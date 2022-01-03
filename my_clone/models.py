from django.db import models


# Create your models here.


class Search(models.Model):
    """
    database models
    """
    search_field = models.CharField(max_length=500)
    search_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search_field)

    class Meta:
        """
        fixing word search in the database
        """
        verbose_name_plural = 'Searches'
