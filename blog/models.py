from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
class blogmodel(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(upload_to="img/",null=True)
    title=models.CharField(max_length=100)
    content=models.CharField()
    category=models.CharField()
    dateandtime=models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title
    

class commentmodel(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    blog=models.ForeignKey(blogmodel,on_delete=models.CASCADE,blank=True,null=True)
    comment=models.CharField()
    dateandtime=models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.blog.title} - {self.user.username}"
    
    
class profilemodel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    userimage=models.ImageField(upload_to="profile/",blank=True,null=True)
    
    
    def __str__(self):
        return self.user.username
    # User.objects.filter(likemodel__blog=some_blog)

    
class likemodel(models.Model):
    user=models.ForeignKey(User ,on_delete=models.CASCADE)
    blog=models.ForeignKey(blogmodel ,on_delete=models.CASCADE)
    liked_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"
    class Meta:
        unique_together=('user','blog')
