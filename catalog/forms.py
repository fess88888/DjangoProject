from django import forms
from .models import Product


FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_name", "product_description", "price", "category", "picture"]

    def clean_product_name(self):
        name = self.cleaned_data.get("product_name", "")
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(
                    f"Название содержит запрещённое слово: «{word}»."
                )
        return name

    def clean_product_description(self):
        description = self.cleaned_data.get("product_description", "")
        description_lower = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise forms.ValidationError(
                    f"Описание содержит запрещённое слово: «{word}»."
                )
        return description
