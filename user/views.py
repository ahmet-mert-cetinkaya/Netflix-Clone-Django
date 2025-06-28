from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import threading
# Create your views here.

def userRegister(request):
    # form = UserForm()
    # if request.method == "POST":
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, "Kayıt Başarılı")
    #         return redirect('login')
    # context = {
    #     'form':form
    # }
    if request.method == "POST":
        isim = request.POST['isim']
        soyisim = request.POST['soyisim']
        email = request.POST['email']
        resim = request.FILES['resim']
        tel = request.POST['tel']
        dogum = request.POST['dogum']
        sifre1 = request.POST['sifre1']
        sifre2 = request.POST['sifre2']

        if sifre1==sifre2:
            if User.objects.filter(email=email).exists():
                messages.error(request,"Bu Email Zaten Kullanılıyor.")
                return redirect("register")

            elif len(sifre1) < 6:
                messages.error(request,"Şifre 6 Karakterden Kısa Olamaz.")
                return redirect("register")
            
            elif "!" in isim or "?" in isim or "=" in isim:
                messages.error(request,"İsimde Özel Karakterler Bulunamaz.")
                return redirect("register")

            else:
                user = User.objects.create_user(username=isim, email=email,password=sifre1)
                Kullanici.objects.create(
                    user = user,
                    isim=isim,
                    soyisim=soyisim,
                    email=email,
                    resim=resim,
                    tel = tel,
                    dogum = dogum,
                )
                subject = "Netflix Clone"
                message = f"Tebrikler {isim} {soyisim}. Netflix Clone hesabınız başarıyla oluşturuldu."
                mail_thread = threading.Thread(target=send_mail, args=(subject, message, settings.EMAIL_HOST_USER, [user.email]))
                mail_thread.start()
                user.save()
                messages.success(request,"Kullanıcı Oluşturuldu.")
                return redirect("login")    
    return render(request,"register.html")

def userLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Başarıyla Giriş Yaptınız.")
            return redirect('profiles')
        else:
            messages.error(request, "Kullanıcı Adı veya Şifre Hatalı!")
            return redirect('login')

    return render(request, 'login.html')

def userLogout(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yapıldı.")
    return redirect("login")

def profiles(request):
    profiller = Profiles.objects.filter(owner = request.user)
    context = {
        'profiller': profiller
    }
    return render(request, "browse.html", context)


def createProfil(request):
    form = ProfilForm()
    if request.method == "POST":
        form = ProfilForm(request.POST, request.FILES)
        if form.is_valid():
            profil = form.save(commit=False)
            profil.owner = request.user
            profil.save()
            messages.success(request, "Profil Oluşturuldu.")
            return redirect('profiles')
    
    context = {
        'form':form
    }

    return render(request, 'create.html', context)

def hesap(request):
    user = request.user.kullanici
    context = {
        'user' : user
    }
    return render(request, "hesap.html", context)