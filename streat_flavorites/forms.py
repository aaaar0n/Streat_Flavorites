from django import forms
from .models import Item, Subcategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.select_related('category')

        # Optionally, you can customize the display of the subcategories in the dropdown
        self.fields['subcategory'].label_from_instance = lambda obj: f"{obj.name} ({obj.category})"


class CheckoutForm(forms.Form):
    user_name = forms.CharField(label='Full Name', max_length=100)
    user_email = forms.EmailField(label='Your Email')
    contact_number = forms.CharField(label='Contact Number', max_length=20)  # Adjust max length as needed
    delivery_address = forms.CharField(label='Delivery Address', widget=forms.Textarea)
    
    # Add any other fields you need for the checkout process
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email