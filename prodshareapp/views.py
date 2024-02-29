from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Post, Category, question, Like, LikeForQuestion, CustomUser, UserProfile, Comment, commentForQuestion
from .forms import PostForm, QuestionForm, searchForm, userprofileForm, CommentForm, commentForQuestionForm
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, Count

# Create your views here.
def homefunc(request):
    context = {}
    posts = Post.objects.all()

    #ページネーション
    paginator = Paginator(posts, 5)
    number = int(request.GET.get("page", "1"))
    post_page = paginator.page(number)

    # いいね
    like_posts = []
    if request.user.is_authenticated:
        for post in posts:
            if post.like_set.filter(user=request.user).exists():
                like_posts.append(post)

    #横のカテゴリ
    category_post_sorted = []
    for category in Category.objects.annotate(category_count=Count("post")).order_by("-category_count")[:10]:
        category_post_sorted.append((category.pk, category, category.category_count))

    context = {
        "num_pages": paginator.num_pages,
        "post_page": post_page,
        "like_posts": like_posts,
        "category_post_sorted": category_post_sorted,
        "form": searchForm()
    }
    return render(request, "home.html", context)

def postDetailfunc(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post.pk)

    if request.user.is_authenticated and post.like_set.filter(user=request.user).exists():
        is_user_liked = True
    else:
        is_user_liked = False


    if request.method == "POST":
        form = CommentForm(request.POST)
        comment = form.save(commit=False)
        comment.writer_id = request.user.id
        comment.post_id = pk
        comment.save()

        return redirect("postdetail", pk=post.pk)

    form = CommentForm()

    context = {
        "is_user_liked": is_user_liked,
        "post": post,
        "comments": comments,
        "form": form
    }

    return render(request, "post_detail.html", context)


def questionListfunc(request):
    question_posts = question.objects.all()

    #ページネーション
    paginator = Paginator(question_posts, 5)
    number = int(request.GET.get("page", "1"))
    question_post_page = paginator.page(number)

    # いいね
    like_posts = []
    if request.user.is_authenticated:
        for question_post in question_posts:
            if question_post.likeforquestion_set.filter(user=request.user).exists():
                like_posts.append(question_post)

    #横のカテゴリ
    category_post_sorted = []
    for category in Category.objects.annotate(category_count=Count("question")).order_by("-category_count")[:10]:
        category_post_sorted.append((category.pk, category, category.category_count))

    context = {
        "num_pages": paginator.num_pages,
        "question_post_page": question_post_page,
        "like_posts": like_posts,
        "category_post_sorted": category_post_sorted,
        "form": searchForm()
    }

    return render(request, "question_list.html", context)

def questionDetailfunc(request, pk):
    question_post = get_object_or_404(question, pk=pk)
    comments = commentForQuestion.objects.filter(question=question_post.pk)

    if request.user.is_authenticated and question_post.likeforquestion_set.filter(user=request.user).exists():
        is_user_liked = True
    else:
        is_user_liked = False

    if request.method == "POST":
        form = commentForQuestionForm(request.POST)
        comment = form.save(commit=False)
        comment.writer_id = request.user.id
        comment.question_id = pk
        comment.save()

        return redirect("questiondetail", pk=question_post.pk)


    form = commentForQuestionForm()
    
    context = {
        "is_user_liked": is_user_liked,
        "question_post": question_post,
        "comments": comments,
        "form": form
    }
    return render(request, "question_detail.html", context)

def categoryPostfunc(request, pk):
    # 後で検索機能追加
    form = searchForm()
    posts = Post.objects.filter(category__id=pk)
    categoryname = Category.objects.get(id=pk)

    #ページネーション
    paginator = Paginator(posts, 5)
    number = int(request.GET.get("page", "1"))
    post_page = paginator.page(number)
    num_pages = paginator.num_pages

    like_posts = []
    if request.user.is_authenticated:
        for post in posts:
            if post.like_set.filter(user=request.user).exists():
                like_posts.append(post)

    context = {
        "categoryname": categoryname,
        "form": form,
        "like_posts": like_posts,
        "post_page": post_page,
        "num_pages": num_pages,
        "posts_num": len(posts)
    }
    return render(request, "category_post.html", context)

def categoryQuestionfunc(request, pk):
    # 後で検索機能追加
    form = searchForm()
    question_posts = question.objects.filter(category__id=pk)
    categoryname = Category.objects.get(id=pk)

    #ページネーション
    paginator = Paginator(question_posts, 5)
    number = int(request.GET.get("page", "1"))
    question_post_page = paginator.page(number)
    num_pages = paginator.num_pages

    like_posts = []
    if request.user.is_authenticated:
        for question_post in question_posts:
            if question_post.likeforquestion_set.filter(user=request.user).exists():
                like_posts.append(question_post)

    context = {
        "categoryname": categoryname,
        "form": form,
        "like_posts": like_posts,
        "question_post_page": question_post_page,
        "num_pages": num_pages,
        "question_posts_num": len(question_posts)
    }
    return render(request, "category_question.html", context)

def searchpostfunc(request):
    keywords = request.GET.get("keywords").replace("　"," ").split(" ")
    query = Q()
    for keyword in keywords:
        query |= Q(title__contains=keyword)
        query |= Q(category__categoryname__contains=keyword)

    posts = Post.objects.filter(query).order_by("id")
 
    #ページネーション
    paginator = Paginator(posts, 3)
    number = int(request.GET.get("page", "1"))
    post_page = paginator.page(number)
    num_pages = paginator.num_pages

    # いいね
    like_posts = []
    if request.user.is_authenticated:
        for post in posts:
            if post.like_set.filter(user=request.user).exists():
                like_posts.append(post)

    #横のカテゴリ
    category_post_sorted = []
    for category in Category.objects.annotate(category_count=Count("post")).order_by("-category_count")[:10]:
        category_post_sorted.append((category.pk, category, category.category_count))

    context = {
        "keywords": keywords,
        "keywordsjson": json.dumps(keywords),
        "posts_num": len(posts),
        "post_page": post_page,
        "num_pages": num_pages,
        "like_posts": like_posts,
        "category_post_sorted": category_post_sorted,
        "form": searchForm()
    }

    return render(request, "search_post.html", context)

def searchquestionfunc(request):
    # 検索処理
    keywords = request.GET.get("keywords").replace("　"," ").split(" ")
    query = Q()
    for keyword in keywords:
        query |= Q(title__contains=keyword)
        query |= Q(category__categoryname__contains=keyword)

    question_posts = question.objects.filter(query).order_by("id")
 
    #ページネーション
    paginator = Paginator(question_posts, 3)
    number = int(request.GET.get("page", "1"))
    question_post_page = paginator.page(number)
    num_pages = paginator.num_pages

    # いいね
    like_question_posts = []
    if request.user.is_authenticated:
        for question_post in question_posts:
            if question_post.likeforquestion_set.filter(user=request.user).exists():
                like_question_posts.append(question_post)

    #横のカテゴリ
    category_post_sorted = []
    for category in Category.objects.annotate(category_count=Count("question")).order_by("-category_count")[:10]:
        category_post_sorted.append((category.pk, category, category.category_count))


    context = {
        "keywords": keywords,
        "keywordsjson": json.dumps(keywords),
        "posts_num": len(question_posts),
        "num_pages": num_pages,
        "question_post_page": question_post_page,
        "like_question_posts": like_question_posts,
        "category_post_sorted": category_post_sorted,
        "form": searchForm()
    }

    return render(request, "search_question.html", context)

@login_required
def postCreatefunc(request):
    categorys = Category.objects.all()
    categorys = list(map(lambda category: category.categoryname, categorys))
    categorys_data = {
        "categorys": categorys
    }
    categorys_data = json.dumps(categorys_data)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            cleaned_categorys = form.cleaned_data["category"].split()
            target_categorys = []
            post = form.instance
            #ここはログイン者にする
            post.writer_id = request.user.id
            post.save()
            for cleaned_category in cleaned_categorys:
                category, iscreated = Category.objects.get_or_create(categoryname=cleaned_category)
                if iscreated:
                    new_category = Category.objects.get(categoryname=cleaned_category)
                    target_categorys.append(new_category)
                else:
                    target_categorys.append(category)
            for target_category in target_categorys:
                post.category.add(target_category)
            post.save()
            return redirect("postdetail", pk=post.pk)
        else:
            form = PostForm()
            context = {
                "form": form,
                "categorys_data": categorys_data
            }
            return render(request, "post_create.html", context)
    else:
        form = PostForm()
        context = {
            "form": form,
            "categorys_data": categorys_data
        }
        return render(request, "post_create.html", context)

def postUpdatefunc(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            cleaned_categorys = form.cleaned_data["category"].split()
            target_categorys = []
            updated_post = form.instance
            #ここはログイン者にする
            updated_post.writer_id = request.user.id
            updated_post.save()
            for cleaned_category in cleaned_categorys:
                category, iscreated = Category.objects.get_or_create(categoryname=cleaned_category)
                if iscreated:
                    new_category = Category.objects.get(categoryname=cleaned_category)
                    target_categorys.append(new_category)
                else:
                    target_categorys.append(category)
            for target_category in target_categorys:
                updated_post.category.add(target_category)
            updated_post.save()
    else:
        result = ""
        category_list = list(map(lambda category: category.categoryname, post.category.all()))
        for category in category_list:
            result += category + " "           
        initial = {
            "title": post.title,
            "content": post.content,
            "category": result
        }
        # form = PostForm(instance=post)
        form = PostForm(initial=initial)

    categorys = Category.objects.all()
    categorys = list(map(lambda category: category.categoryname, categorys))
    categorys_data = {
        "categorys": categorys
    }

    categorys_data = json.dumps(categorys_data)

    context = {
        "form": form,
        "categorys_data": categorys_data
    }
    return render(request, "post_update.html", context)
    

@login_required
def questionCreatefunc(request):
    categorys = Category.objects.all()
    categorys = list(map(lambda category: category.categoryname, categorys))
    categorys_data = {
        "categorys": categorys
    }
    categorys_data = json.dumps(categorys_data)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            cleaned_categorys = form.cleaned_data["category"].split()
            target_categorys = []
            question_post = form.instance
            #ここはログイン者にする
            question_post.writer_id = request.user.id
            question_post.save()
            for cleaned_category in cleaned_categorys:
                category, iscreated = Category.objects.get_or_create(categoryname=cleaned_category)
                if iscreated:
                    new_category = Category.objects.get(categoryname=cleaned_category)
                    target_categorys.append(new_category)
                else:
                    target_categorys.append(category)
            for target_category in target_categorys:
                question_post.category.add(target_category)
            question_post.save()
            return redirect("questiondetail", pk=question_post.pk)
        else:
            form = QuestionForm()
            context = {
                "form": form,
                "categorys_data": categorys_data
            }
            return render(request, "question_create.html", context)
    else:
        form = QuestionForm()
        context = {
            "form": form,
            "categorys_data": categorys_data
        }
        return render(request, "question_create.html", context)


def questionUpdatefunc(request, pk):
    question_post = get_object_or_404(question, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question_post)
        if form.is_valid():
            cleaned_categorys = form.cleaned_data["category"].split()
            target_categorys = []
            updated_question_post = form.instance
            #ここはログイン者にする
            updated_question_post.writer_id = request.user.id
            updated_question_post.save()
            for cleaned_category in cleaned_categorys:
                category, iscreated = Category.objects.get_or_create(categoryname=cleaned_category)
                if iscreated:
                    new_category = Category.objects.get(categoryname=cleaned_category)
                    target_categorys.append(new_category)
                else:
                    target_categorys.append(category)
            for target_category in target_categorys:
                updated_question_post.category.add(target_category)
            updated_question_post.save()
    else:
        result = ""
        category_list = list(map(lambda category: category.categoryname, question_post.category.all()))
        for category in category_list:
            result += category + " "           
        initial = {
            "title": question_post.title,
            "content": question_post.content,
            "category": result
        }
        # form = PostForm(instance=post)
        form = QuestionForm(initial=initial)

    categorys = Category.objects.all()
    categorys = list(map(lambda category: category.categoryname, categorys))
    categorys_data = {
        "categorys": categorys
    }
    categorys_data = json.dumps(categorys_data)

    context = {
        "form": form,
        "categorys_data": categorys_data
    }
    return render(request, "question_update.html", context)

def postdeletefunc(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('home')

def questiondeletefunc(request, pk):
    question_post = get_object_or_404(question, pk=pk)
    question_post.delete()
    return redirect('questionlist')

def postcommentdeletefunc(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    comment.delete()
    return redirect("postdetail", post.id)

def questioncommentdeletefunc(request, pk):
    print("a")
    comment = get_object_or_404(commentForQuestion, pk=pk)
    question_post = comment.question
    comment.delete()
    return redirect("questiondetail", question_post.id)

def profilefunc(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        userprofile = getattr(user, "profile", None)
        if userprofile:
            form = userprofileForm(request.POST, request.FILES, instance=userprofile)
        else:
            form = userprofileForm(request.POST, request.FILES)
        

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile', pk)  # 画像一覧ページにリダイレクト
    user_posts = user.post_set.all()
    user_question_posts = user.question_set.all()
    user_post_amount = len(user_posts)
    user_question_post_amount = len(user_question_posts)

    # 投稿ページネーション
    paginator_post = Paginator(user_posts, 3)
    number = int(request.GET.get("page", "1"))
    num_pages_post = paginator_post.num_pages
    try:
        user_post_page = paginator_post.page(number)
    except EmptyPage:
        user_post_page = paginator_post.page(1)



    like_user_posts = []
    if request.user.is_authenticated:
        for user_post in user_posts:
            if user_post.like_set.filter(user=request.user).exists():
                like_user_posts.append(user_post)

    # 質問ページネーション
    paginator_question_post = Paginator(user_question_posts, 3)
    number = int(request.GET.get("page", "1"))
    num_pages_question_post = paginator_question_post.num_pages
    try:
        user_question_post_page = paginator_question_post.page(number)
    except EmptyPage:
        user_question_post_page = paginator_question_post.page(1)

    like_user_question_posts = []
    if request.user.is_authenticated:
        for user_question_post in user_question_posts:
            if user_question_post.likeforquestion_set.filter(user=request.user).exists():
                like_user_question_posts.append(user_question_post)

    context = {
        "user": user,
        "user_post_page": user_post_page,
        "user_question_post_page": user_question_post_page,
        "user_post_amount": user_post_amount,
        "user_question_post_amount": user_question_post_amount,
        "like_user_posts": like_user_posts,
        "like_user_question_posts": like_user_question_posts,
        "num_pages_post":num_pages_post,
        "num_pages_question_post":num_pages_question_post,
        "userprofileform": userprofileForm()
    }
    return render(request, "profile.html", context)



# jsから受け取る関数
def likefunc(request):
    context = {}
    post_pk = request.POST.get('post_pk')
    post = get_object_or_404(Post, pk=post_pk)
    like = Like.objects.filter(targetpost=post, user=request.user)

    #既にイイねしていたら削除、していなかったらイイね
    if like.exists():
        like.delete()
        method = "delete"
    else:
        like.create(targetpost=post, user=request.user)
        method = "create"

    context = {
        'method': method,
        'like_count': post.like_set.count()
    }

    return JsonResponse(context)

def likeforquestionfunc(request):
    context = {}
    question_post_pk = request.POST.get('question_post_pk')
    question_post = get_object_or_404(question, pk=question_post_pk)
    like = LikeForQuestion.objects.filter(targetquestion=question_post, user=request.user)

    #既にイイねしていたら削除、していなかったらイイね
    if like.exists():
        like.delete()
        method = 'delete'
    else:
        like.create(targetquestion=question_post, user=request.user)
        method = 'create'

    context = {
        "method": method,
        "like_count": question_post.likeforquestion_set.count()
    }

    return JsonResponse(context)
