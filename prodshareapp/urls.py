from django.contrib import admin
from django.urls import path
from .views import (
    homefunc, postDetailfunc, 
    questionListfunc, questionDetailfunc, categoryPostfunc, 
    categoryQuestionfunc,searchpostfunc, searchquestionfunc, 
    postCreatefunc, postUpdatefunc, 
    questionCreatefunc, questionUpdatefunc, profilefunc, likefunc,
    likeforquestionfunc, 
    postdeletefunc, questiondeletefunc, postcommentdeletefunc, questioncommentdeletefunc
)

urlpatterns = [
    path('home/', homefunc, name="home"),
    path('post/detail/<int:pk>', postDetailfunc, name="postdetail"),
    path('post/update/<int:pk>', postUpdatefunc, name="postupdate"),
    path('post/create/', postCreatefunc, name="postcreate"),
    path('post/delete/<int:pk>', postdeletefunc, name="postdelete"),
    path('post/comment/delete/<int:pk>', postcommentdeletefunc, name="postcommentdelete"),

    path('question_list/', questionListfunc, name="questionlist"),
    path('question/detail/<int:pk>', questionDetailfunc, name="questiondetail"),
    path('question/update/<int:pk>', questionUpdatefunc, name="questionupdate"),
    path('question/create/', questionCreatefunc, name="questioncreate"),
    path('question/delete/<int:pk>', questiondeletefunc, name="questiondelete"),
    path('question/comment/delete/<int:pk>', questioncommentdeletefunc, name="questioncommentdelete"),

    path('category_post/<int:pk>', categoryPostfunc, name="categorypost"),
    path('category_question/<int:pk>', categoryQuestionfunc, name="categoryquestion"),

    path('search/post', searchpostfunc, name="searchpost"),
    path('search/question', searchquestionfunc, name="searchquestion"),

    path('profile/<int:pk>', profilefunc, name="profile"),
    
    path('like/', likefunc, name="like"),
    path('likeforquestion/', likeforquestionfunc, name="likeforquestion"),
]