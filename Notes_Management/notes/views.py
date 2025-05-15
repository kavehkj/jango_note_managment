from django.views.generic import TemplateView ,DetailView ,DeleteView , UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView ,CreateView
from django.contrib.auth import login
from .forms import SignupForm , LoginForm , add_note
from django.contrib.auth.views import LoginView, LogoutView
from .models import Note
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now


class home(TemplateView):
    template_name = 'notes/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_notes'] = Note.objects.filter(status=True).order_by('-created_at')[:3]
        return context


class list_note(TemplateView):
    template_name = 'notes/note_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_notes'] = Note.objects.filter(status=True).order_by('-created_at')
        return context



class add_note(LoginRequiredMixin,CreateView):
    template_name = 'notes/add_note.html'
    model = Note
    form_class = add_note
    success_url = reverse_lazy('add_note')

    login_url = reverse_lazy('login')

    def form_valid(self, form):
        # تخصیص خودکار کاربر به فیلد user
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super().form_valid(form)



class user_list(TemplateView):  
    template_name = 'notes/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = Note.objects.filter(user=self.request.user).order_by('-created_at')
        return context



class note_detail(DetailView):
    model = Note
    slug_field = 'slug'
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'



class edit_note(UpdateView):
    model = Note
    slug_field = 'slug'
    fields = ['title', 'content', 'status', 'image']
    template_name = 'notes/note_edite.html'
    success_url = reverse_lazy('user_list')
    def form_valid(self, form):
        # مقداردهی به فیلد last_edited قبل از ذخیره
        form.instance.updated_at = now()
        return super().form_valid(form)





class delete_note(DeleteView): 
    model = Note
    slug_field = 'slug'
    success_url = reverse_lazy('user_list')
    template_name = 'notes/note_delete.html'


class CustomLogin(LoginView):
    template_name = "notes/login.html"
    authentication_form = LoginForm 
    redirect_authenticated_user = True 

    def get_success_url(self):
        return reverse_lazy("home")  
   

class signup(FormView):
    template_name = "notes/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])  # هش کردن رمز عبور
        user.save()
        login(self.request, user)  # لاگین کردن کاربر بعد از ثبت‌نام
        return super().form_valid(form)


class CustomLogout(LogoutView):
    next_page = reverse_lazy("home")

