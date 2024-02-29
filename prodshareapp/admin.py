from django.contrib import admin
from .models import CustomUser, UserProfile, Category, Post, Comment, Like, question, commentForQuestion, LikeForQuestion
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(question)
admin.site.register(commentForQuestion)
admin.site.register(LikeForQuestion)