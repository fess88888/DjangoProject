from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import BlogPost


class BlogPostListView(ListView):
    """Список только опубликованных статей."""
    model = BlogPost
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Выводим только статьи с признаком публикации."""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Детальная страница статьи + счётчик просмотров."""
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Увеличиваем счётчик просмотров при каждом открытии статьи."""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        # Дополнительное задание: поздравление при 100 просмотрах
        if obj.views_count == 100:
            from django.core.mail import send_mail
            from django.conf import settings

            send_mail(
                subject="Поздравляем с 100 просмотрами!",
                message=f'Статья "{obj.title}" достигла 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
            )

        return obj


class BlogPostCreateView(CreateView):
    """Создание статьи."""
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:post_list")


class BlogPostUpdateView(UpdateView):
    """Редактирование статьи."""
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def get_success_url(self):
        """После редактирования — на страницу отредактированной статьи."""
        return reverse("blog:blogpost_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Удаление статьи."""
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("blog:blogpost_list")
