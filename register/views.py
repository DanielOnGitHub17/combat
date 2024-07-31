from django.contrib import messages as msg
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic.edit import CreateView

from game.models import Player
from helpers import handle_error, WoodenError, new_username
from register.forms import SignInForm, SignUpForm


class Profile(LoginRequiredMixin, View):
    def post(self, request):
        if len(request.POST) > 1:
            # for
            return
        return redirect("/profile/")

    def get(self, request):
        return render(request, "profile.html", {})

class SignUp(SuccessMessageMixin, CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = "/signin/"
    success_message = "Hello, %(first_name)s. Your account was created successfully. Please click the link in your email to verify your account."

    def form_valid(self, form):
        try:
            # Create User and assign to new Player
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            Player(user=new_user).save()
            self.request.session["user_id"] = new_user.pk
            Confirm.send_confirmation_email(new_user, self.request.scheme, self.request.get_host())
        finally:
            return super().form_valid(form)

    def form_invalid(self, form):
        if "username" in form.errors and form.errors["username"][0].endswith("username already exists."):  # Ha!
            msg.add_message(self.request, msg.ERROR, f"Username {form.data['username']} is taken. How about {new_username(form.data['first_name'])}?")
        return super().form_invalid(form)
    
    def get(self, request):
        return redirect("/lounge/") if self.request.user.is_authenticated else super().get(request)

class SignIn(SuccessMessageMixin, LoginView):
    template_name = "signin.html"
    success_message = "Signin successful!"
    redirect_authenticated_user = True
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            player = self.request.user.player
            player.logged_in = True
            player.score = 0
            player.save()
        return super().dispatch(*args, **kwargs)


class SignOut(LoginRequiredMixin, LogoutView):
    template_name = "signed_out.html"
    LogoutView.http_method_names.append("get")  # HA!

    def post(self, request):
        player = request.user.player
        if player.game:
            return self.get(request)
        player.logged_in = False
        player.save()
        return super().post(request)
    
    def get(self, request):
        print(self.request.build_absolute_uri())
        if request.user.player.game:
            msg.add_message(request, msg.ERROR, "You cannot sign out now. You are in a game")
            return redirect("/lounge/")
        return render(request, "signout.html")


class Confirm(View):
    def post(self, request):
        # send activation email
        if "user_id" not in request.session:
            try:
                new_user = User.objects.get(pk=request.session["user_id"])
                if new_user.is_active:
                    msg.add_message(request, msg.INFO, "Your account is already activated.")
                else:
                    Confirm.send_confirmation_email(new_user, request.scheme, request.get_host())
            except:
                del request.session["user_id"]
        else:
            msg.add_message("That page is inaccessible")
        
        return redirect("/signin/")
    
    @staticmethod
    def send_confirmation_email(new_user, scheme, host):
        uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
        token = account_activation_token.make_token(new_user)
        activate_url = f"{scheme}://{host}/activate/{uidb64}/{token}/"
        context = {
            "user": new_user,
            "activate_url": activate_url
        }
        email_html_message = render_to_string("account_activation_email.html", context)
        email = EmailMessage(
            subject="Wooden: Activate Your Account",
            body=email_html_message,
            to=[new_user.email]
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)


class ResetPassword(PasswordResetView):
    template_name = "password_reset_form.html"
    html_email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"

class DoneResetPassword(PasswordResetDoneView):
    template_name = "password_reset_done.html"

class ConfirmResetPassword(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    success_url = "/signin/"
    success_message = "Your password was changed successfully. Please log in."


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) + str(timestamp) + str(user.is_active))

account_activation_token = AccountActivationTokenGenerator()

def activate(request, uidb64, token):
    try:
        uid = smart_str(urlsafe_base64_decode(uidb64).decode('utf-8'))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        msg.add_message(request, msg.SUCCESS, "Your wooden account has been successfuly activated. Please log in")
        if "user_id" in request.session:
            del request.session["user_id"]
        return redirect("/signin/")
    
    msg.add_message(request, msg.ERROR, "Sorry, but your wooden account could not be validated. Please retry creating an account")
    return redirect("/signup/")