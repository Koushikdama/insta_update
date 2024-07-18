from django import forms
from Post.models import Post

from django.forms import ClearableFileInput




class NewPostForm(forms.ModelForm):
	
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
	tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)

	class Meta:
		model = Post
		fields = ('caption', 'tags')
		