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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
        self.fields["product_name"].widget.attrs["placeholder"] = "Введите название"
        self.fields["product_description"].widget.attrs["placeholder"] = "Введите описание"
        self.fields["price"].widget.attrs["placeholder"] = "Введите цену"
        self.fields["picture"].widget.attrs["class"] = "form-control-file"

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

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None:
            raise forms.ValidationError("Укажите цену продукта.")
        if price < 0:
            raise forms.ValidationError(
                "Цена не может быть отрицательной. "
                "Укажите значение больше или равно нулю."
            )
        return price

    def clean_picture(self):
        picture = self.cleaned_data.get("picture")
        if not picture:
            return picture  # поле необязательное — пусто, значит ОК

        # Проверка размера (5 МБ = 5 * 1024 * 1024 байт)
        max_size = 5 * 1024 * 1024
        if picture.size > max_size:
            raise forms.ValidationError(
                "Размер изображения не должен превышать 5 МБ."
            )

        # Проверка формата
        valid_formats = ["image/jpeg", "image/png"]
        if hasattr(picture, "content_type"):
            if picture.content_type not in valid_formats:
                raise forms.ValidationError(
                    "Допустимые форматы изображения: JPEG или PNG."
                )
        return picture
