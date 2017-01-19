from django.db import models


class Cities(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return '{}, {}'.format(self.city, self.state)
    pass


class EmailList(models.Model):
    email_address = models.CharField(max_length=100, unique=True)
    location_id = models.ForeignKey(Cities, on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}'.format(self.email_address, self.location_id)
