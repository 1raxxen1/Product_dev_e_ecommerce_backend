from django.db import models
from django.utils.text import slugify

# Create your models here.
# to do
# image-text-image 
# keywords

class BlogCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Keyword(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nam


class BlogPost(models.Model):

    id = models.BigAutoField(primary_key=True)

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField()

    cover_image = models.ImageField(
        upload_to='blog_covers/', 
        null=True, blank=True
    )

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts"
    )

    keywords = models.ManyToManyField(
        Keyword,
        related_name="posts",
        blank=True
    )


    is_published = models.BooleanField(default=True)
    publised_at = models.DateTimeField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogContentBlock(models.Model):
    TEXT = "text"
    IMAGE = "image"

    BLOCK_TYPE_CHOICES = [
        (TEXT, "Text"),
        (IMAGE, "Image"),
    ]

    id = models.BigAutoField(primary_key=True)

    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="content_blocks"
    )

    block_type = models.CharField(
        max_length=10,
        choices=BLOCK_TYPE_CHOICES
    )

    rich_text = models.JSONField(blank=True, null=True)

    image = models.ImageField(
        upload_to="blog/blocks/",
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ("post", "order")

    def __str__(self):
        return f"{self.post.title} - {self.block_type} [{self.order}]"
    


