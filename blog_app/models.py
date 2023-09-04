from django.db import models


class Author(models.Model):
    """ Author model holds information about a author """

    name = models.CharField(max_length=255)
    about = models.TextField()
    joined_on = models.DateField(auto_now_add=True)
    picture = models.ImageField(null=True)

    def __str__(self):
        return f"{self.name} {self.joined_on}"


class Post(models.Model):
    """ Post model holds information about a post which is created by a author """

    title = models.CharField(max_length=255)
    date = models.DateField(auto_now=True)
    detail = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    picture = models.ImageField(null=True)

    def __str__(self):
        return f"{self.title} {self.date} {self.author}"


class Comment(models.Model):
    """ Comment model holds information about each comment made on a particular post """
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    commented_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} {self.email} {self.commented_on}"


class Tag(models.Model):
    """ Tag model holds information about tags """
    label = models.CharField(max_length=255, unique=True)
    post = models.ManyToManyField(Post)

    def __str__(self):
        return f"{self.label}"
