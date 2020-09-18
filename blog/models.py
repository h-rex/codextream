from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
from django.utils.timezone import now


class CategoryBlog(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        # enforcing that there can not be two categories under a parent with same slug
        # __str__ method elaborated later in post.  use __unicode__ in place of
        # __str__ if you are using python 2
        unique_together = ['slug']
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse('blog:list_of_post_by_category', args=[self.slug])

    def __str__(self):
        return self.slug


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    img = models.ImageField(upload_to='thumbnails')
    slug = models.SlugField(max_length=300, null=True, blank=True, unique=True)
    body_text = RichTextUploadingField(null=True)
    category = models.ForeignKey(CategoryBlog, null=True, blank=True, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)


    class Meta:
        ordering = ['-pk']
        
    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category  # for now ignore this instance method

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comm = models.TextField()


class SubCommnet(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    comm = models.TextField()
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
