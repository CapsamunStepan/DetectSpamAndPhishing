from django import forms


class GmailCredentialsForm(forms.Form):
    gmail = forms.CharField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    oauth2_key = forms.CharField(label='API Key', widget=forms.TextInput(attrs={'class': 'form-control'}))
