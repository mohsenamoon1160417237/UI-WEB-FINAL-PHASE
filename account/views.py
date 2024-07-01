import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Case, When, Value, BooleanField
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegisterForm
from .models import MyUser
from utils.token import account_activation_token
from object_storage.models import UserObjectStorage


@login_required
def home(request):
    if request.method == "GET":
        user = request.user
        query = request.GET.get("query")
        if not query:
            usr_objects = UserObjectStorage.objects.all()
        else:
            usr_objects = UserObjectStorage.objects.filter(file_name__icontains=query)
        user_objects1 = usr_objects.filter(user=user)
        user_objects2 = usr_objects.filter(
            ~Q(id__in=user_objects1.values('id')),
            users_added__id__in=[user.id]
        )
        user_objects = usr_objects.filter(
            id__in=[*user_objects1.values_list('id', flat=True),
                    *user_objects2.values_list('id', flat=True)]
        )
        user_objects = user_objects.annotate(
            owner=Case(
                When(Q(user=user), then=Value(True)),
                When(Q(users_added__in=[user]), then=Value(False)),
                output_field=BooleanField()
            )).order_by('uploaded_date_time')
        user_object_ids = user_objects.values('id').distinct()
        user_objs = {}
        for obj in user_object_ids:
            for user_obj in user_objects:
                if obj.get('id') == user_obj.id:
                    if obj.get('id') not in user_objs:
                        user_objs[obj.get('id')] = {'file_name': user_obj.file_name,
                                                    'file_size': user_obj.file_size,
                                                    'uploaded_date_time': user_obj.uploaded_date_time,
                                                    'user': user_obj.user,
                                                    'owner': user_obj.owner,
                                                    'id': user_obj.id,
                                                    'extension': user_obj.file_name.split(".")[-1]}
        total_size = sum([x.get('file_size') for x in user_objs.values()])
        page = request.GET.get('page', 1)
        paginator = Paginator(list(user_objs.values()), 8)
        try:
            user_objs = paginator.page(page)
        except PageNotAnInteger:
            user_objs = paginator.page(1)
        except EmptyPage:
            user_objs = paginator.page(paginator.num_pages)

        people = MyUser.objects.exclude(id=request.user.id)

        return render(request, 'Dashboard.html',
                      {'owner_objects': user_objs,
                       'people': people,
                       'total_size': total_size})


@login_required
def get_list_of_people_by_file(request, file_id: int):
    if request.method == "GET":
        query = request.GET.get("query")
        if not query:
            users = MyUser.objects.all()
        else:
            users = MyUser.objects.filter(Q(email__icontains=query) | Q(username__icontains=query))
        file = UserObjectStorage.objects.get(id=file_id)
        user = request.user
        people_who_have_perm_for_file = file.users_added.all().filter(id__in=users.values('id')).exclude(id=user.id)
        other_people = users.filter(~Q(id=user.id), ~Q(id__in=people_who_have_perm_for_file.values('id')))
        return render(request, "shareFile.html", {
            "people_who_have_perm_for_file": people_who_have_perm_for_file,
            "other_people": other_people})


def user_register(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        data = {
            'email': data['email'],
            'password': data['password'],
            'username': data['username'].lower()
        }
        register_form = RegisterForm(data=data)
        if register_form.is_valid():
            user = register_form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = register_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect("register")
        else:
            context = {'errors': {
                k: v.data for k, v in register_form.errors.items()}}
            return redirect("register", context=context)
    else:
        return render(request, "CreateAccount.html", context={'errors': {}})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def email_sent(request):
    return render(request, "VerifySent.html")


def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        email = data['username'].lower()
        password = data['password']
        users = MyUser.objects.filter(Q(email=email) | Q(username=email))
        if users.exists():
            user = users.first()
            if user.password == password:
                login(request, user=user)
                return redirect("home")
    else:
        return render(request, "LoginPage.html")


@login_required
def add_people_to_file(request, file_id):
    if request.method == "POST":
        file = UserObjectStorage.objects.get(id=file_id)
        for usr in file.users_added.all():
            file.users_added.remove(usr)
        data = json.loads(request.body.decode("utf-8"))
        for p_id in data:
            file.users_added.add(p_id)
        file.save()
        return redirect("home")
