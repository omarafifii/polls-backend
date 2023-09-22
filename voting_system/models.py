from django.db import models

# Create your models here.
class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    exp_date = models.DateTimeField("Expiry Date")

    class Meta:
        ordering = ["-exp_date"]

    def __str__(self):
        return self.title

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ["-votes"]

    def __str__(self):
        return self.text
    
class Voter(models.Model):
    email = models.EmailField(max_length=200,unique=True)
    polls = models.ManyToManyField(Poll, blank=True)

    def __str__(self):
        return self.email
    
class Confirmation(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    otp = models.CharField(max_length=200)
    isActive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp
