from django import forms
from django.utils.translation import gettext_lazy as _
from catalog.models import Book, Genre, Language
import datetime

class renew_due_back(forms.Form):

    renew_data = forms.DateField(help_text="now to 4weeks later")

    def clean_renew_data(self):
        
        data = self.cleaned_data['renew_data']

        today = datetime.date.today()
        if data < today:
            raise forms.ValidationError(_("cant be past"))
        if data > today + datetime.timedelta(weeks=4):
            raise forms.ValidationError(_("cant be more than 4weeks"))
        
        return data


class BookForm(forms.Form):

    title = forms.CharField(max_length=200, help_text='enter book title', required=True)
    author = forms.ModelChoiceField(queryset=Book.objects.all(), required=True)
    summary = forms.SlugField(help_text='enter summary', required=True)
    isbn = forms.CharField(max_length=13, help_text='enter isbm(13 characters)', required=True)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=True)
    lang = forms.ModelChoiceField(queryset=Language.objects.all(), required=True)
    
    def clean_isbn(self):
        
        data = self.cleaned_data['isbn']

        if len(data) != 13: raise forms.ValidationError(_("invalid isbn code"))
        return data