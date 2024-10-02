from django import forms
from .models import Profile, BlogPost

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image', )
     
        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('título', 'slug', 'content', 'image')
        widgets = {
            'título': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título del Blog'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Copia el título sin espacios y con un guión entre ellos.'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content del Blog'}),
        }