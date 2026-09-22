from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy("catalog:home")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Отправка приветственного письма
            send_mail(
                subject="Добро пожаловать в Skystore!",
                message=f"Здравствуйте, {user.email}!\n\nВы успешно зарегистрировались в нашем магазине. Спасибо, что выбрали нас!",
                from_email=settings.EMAIL_HOST_USER if hasattr(settings, "EMAIL_HOST_USER") else "noreply@skystore.ru",
                recipient_list=[user.email],
                fail_silently=True,
            )
            return redirect("catalog:home")
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {"form": form})
