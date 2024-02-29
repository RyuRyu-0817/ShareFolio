from django import forms
from mdeditor.fields import MDTextFormField
from .models import Category, Post, question, UserProfile, Comment, commentForQuestion

#カテゴリのバリデーション
def validate_confirm(value):
    if len(value) == 0:
        raise forms.ValidationError("カテゴリを選んでください", params={'value': value},)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "category"]

        widgets = {
            'title': forms.TextInput(attrs=
                                    {'class': 'title-input', 
                                     'placeholder': '投稿タイトル'
                                    }),
        }

    category =  forms.CharField(label="aaa", widget=forms.TextInput(attrs={'class': 'category-input', 'placeholder': 'カテゴリを一つ以上指定してください'}), validators=[validate_confirm])

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]

class commentForQuestionForm(forms.ModelForm):

    class Meta:
        model = commentForQuestion
        fields = ["content"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ["title", "content", "category"]

        widgets = {
            'title': forms.TextInput(attrs=
                                    {'class': 'title-input', 
                                     'placeholder': '質問タイトル'
                                    }),
        }
    category =  forms.CharField(label="aaa", widget=forms.TextInput(attrs={'class': 'category-input', 'placeholder': 'カテゴリを一つ以上指定してください'}), validators=[validate_confirm])

class userprofileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["picture"]

    picture = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "profile"}), 
        label=""
    )



class searchForm(forms.Form):
    keywords = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "投稿や質問を検索"}),
        label="", 
        max_length=50
    )
