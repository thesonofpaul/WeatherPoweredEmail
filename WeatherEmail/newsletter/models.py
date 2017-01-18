from django.db import models


class Email_List(models.Model):
    email_address = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(Cities, on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}'.format(self.email_address, self.location)


class Cities(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return '{}, {}'.format(self.city, self.state)