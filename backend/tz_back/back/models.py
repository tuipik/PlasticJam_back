from django.db import models

# Create your models here.


class RepresentableMixin:

    def __str__(self):
        return f'<{self.__class__.__name__}>'


class User(RepresentableMixin, models.Model):

    FEMALE_GENDER = 'Female'
    MALE_GENDER = 'Male'

    GENDER_CHOICES = (
        (FEMALE_GENDER, FEMALE_GENDER),
        (MALE_GENDER, MALE_GENDER),
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=50)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f'{super().__str__()} {self.first_name}'

    @classmethod
    def get_by_id(cls, id_):
        return cls.objects.filter(id=id_).first()


class UserStatistics(RepresentableMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    page_views = models.PositiveIntegerField()
    clicks = models.PositiveIntegerField()

    def __str__(self):
        return f'{super().__str__()} {self.date}'

    @classmethod
    def filter_by_user(cls, user_id):
        return cls.objects.filter(user_id=user_id)
