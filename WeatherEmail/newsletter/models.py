from django.db import models

# stores top 100 cities in US based on population
class Cities(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return '{}, {}'.format(self.city, self.state)

# stores all subscribed email addresses with respective Cities object
class EmailList(models.Model):
    email_address = models.CharField(max_length=100, unique=True, null=False)
    location = models.ForeignKey(Cities, on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}'.format(self.email_address, self.location)
