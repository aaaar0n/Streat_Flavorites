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
