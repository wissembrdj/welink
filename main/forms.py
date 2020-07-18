from django import forms

class UserQuery(forms.Form):
    userquery = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Example: Where is Algeria located?', 'class': 'form-control form-control-lg', 'required': 'required'}))