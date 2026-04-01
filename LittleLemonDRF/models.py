from django.db import models

# Create your models here.
class Category(models.Model):
    # The 'slug' attribute using SlugField
    slug = models.SlugField()

    # The 'title' attribute with a max length of 255
    title = models.CharField(max_length=255)

    # A third attribute (e.g., description) to complete the set
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    # Title with a max length of 225
    title = models.CharField(max_length=225)

    # Price handling up to 9999.99
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Inventory count using a small integer field
    inventory = models.SmallIntegerField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - ${self.price}"
