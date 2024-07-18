from django import forms

from Stories.models import Story

from django.forms.widgets import ClearableFileInput

class NewStoryForm(forms.ModelForm):
	
	caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)

	class Meta:
		model = Story
		fields = ('caption',)