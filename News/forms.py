from django.utils.translation import gettext as _

from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

from .models import Post, Author
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    title = forms.CharField(label=_('Заголовок'), min_length=2, max_length=150)
    text = forms.CharField(label=_('Содержание'), min_length=200)
    # пользователь может добавить нового автора или выбрать уще существующего
    author_name = forms.CharField(label=_('Автор'), required=False)
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        label=_('Автор'),
        empty_label=_('Выберите автора'),
        required=False,
        widget=forms.Select,
    )

    class Meta:
        model = Post
        fields = ['category', 'title', 'text', 'author_name', 'author']
        widgets = {
            'category': forms.CheckboxSelectMultiple,  # можно выбрать 1 и более категорий
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title[0].islower():
            raise forms.ValidationError(
                _("Заголовок должен начинаться с заглавной буквы!")
            )
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if text[0].islower():
            raise forms.ValidationError(
                "Текст долежн начинаться с заглавной буквы!"
            )
        return text

    def clean(self):
        cleaned_data = super().clean()
        author_name = cleaned_data.get('author_name')
        author = cleaned_data.get('author')
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')

        if author_name:
            # проверка не выбран ли автор из списка
            if author:
                raise forms.ValidationError(
                    _("Выберите автора из списка или добавьте нового")
                )

        # если выбран автор из списка
        if author:
            cleaned_data['author_name'] = ''

        if title == text:
            raise forms.ValidationError(
                _("Содержание статьи не должно быть идентичным описанию!")
            )

        return cleaned_data

    def save(self, commit=True):
        post = super().save(commit=False)
        author_name = self.cleaned_data.get('author_name')
        author = self.cleaned_data.get('author')

        if author_name:
            #  создание нового автора
            author, created = Author.objects.get_or_create(
                author__username=author_name,
                defaults={'author': User.objects.create_user(username=author_name, password='password')}
            )

        post.author = author
        if commit:
            post.save()
            self.save_m2m()
        return post


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


