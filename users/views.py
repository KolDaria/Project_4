import secrets

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import ProfileForm, UserRegisterForm
from users.models import User


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        try:
            send_mail(
                subject='Добро пожаловать в наш сервис',
                message=f'Спасибо, что зарегистрировались в нашем сервисе!, '
                        f'перейдите по ссылке для подтверждения почты {url}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except BadHeaderError:
            return HttpResponse('Недопустимое значение')
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile', pk=request.user.pk)
        else:
            context = {'user_form': user_form, 'profile_form': profile_form}
            return render(request, 'edit_profile.html', context)
    else:
        user_form = UserRegisterForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'edit_profile.html', context)


@login_required
def view_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'profile.html', {'user': user})


@login_required
def view_own_profile(request):
    return redirect('users:profile', pk=request.user.pk)


@permission_required("users.can_block_user")
def block_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_blocked = True
    user.save()
    return redirect('users:user_list')


@permission_required('users.can_view_users')
def user_list(request):
    users = User.objects.all()
    return render(request, 'users_list.html', {'users': users})


@permission_required('users.can_block_user')
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user == request.user:
        messages.error(request, "Нельзя заблокировать самого себя.")
    elif user.is_superuser:
        messages.error(request, "Нельзя заблокировать суперпользователя.")
    else:
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f"Пользователь {user.username} "
                                  f"{'заблокирован' if not user.is_active else 'активирован'}.")
    return redirect('users:user_list')
