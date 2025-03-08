from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
class Type(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
class Element(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    description = models.TextField()
    content = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) # 12345678.10

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title