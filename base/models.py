from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content =  RichTextField(blank=True,null=True)
    date_created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)
    ip_address = models.TextField(blank=True)
    views_count = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            while questions.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super(questions, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()
class Comment(models.Model):
    questions = models.ForeignKey(questions, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content =  RichTextField(blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.name


