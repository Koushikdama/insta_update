from django import forms
from Comment.models import Comment

class CommentForm(forms.ModelForm):
	body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea in-put','style':'height:70px' }), required=True)

	class Meta:
		model = Comment
		fields = ('body',)