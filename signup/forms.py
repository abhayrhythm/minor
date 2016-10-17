from django import forms


class NameForm(forms.Form):
    your_name = forms.CharField(label='Name', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'FULL NAME'}))
    your_username = forms.CharField(label='Username', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'USERNAME'}))
    your_email = forms.EmailField(label='Email',max_length=100,widget=forms.TextInput(attrs={'placeholder': 'EMAIL','autocomplete':'off'}))
    your_password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder':'PASSWORD'}),)


class LoginForm(forms.Form):
    nameoremail = forms.CharField(label='Name or Email', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'USERNAME OR EMAIL'}))
    passlogin = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'PASSWORD'}))


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()