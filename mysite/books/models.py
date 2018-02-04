from django.db import models


# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(blank=True, verbose_name='e-mail')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    """
    빈 문자열을 유효한 값(예: 날짜, 시간 및 숫자)으로 허용하지 않는 데이터베이스 열유형과 관련된 예외가 있다.
    빈 문자열을 날짜 또는 정수 열에 삽입하려고 하면 여러분이 사용 중인 데이터베이스에 따라
    데이터베이스 오류가 발생할 수 있다.
    """
    publication_date = models.DateField()

    def __str__(self):
        return self.title
