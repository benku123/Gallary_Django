from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe


class Post(models.Model):
    title = models.CharField(max_length=140, unique=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='posts/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('post_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'pk': self.pk})

    def image_tag(self):
        return mark_safe('<img src="%s"/>' % self.image.url)

    image_tag.allow_tags = True

    # def get_review(self):
    #     return reverse('add_review', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_posted']


class Review(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    email = models.EmailField()
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    post = models.ForeignKey(Post, verbose_name='post', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.post}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'