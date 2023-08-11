from django import forms
from .models import Item, Subcategory

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