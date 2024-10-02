from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages
from .models import Profile


def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "blog.html", {'posts':posts})

def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method=="POST":
        user = request.user
        content = request.POST.get('content','')
        blog_id =request.POST.get('blog_id','')
        comment = Comment(user = user, content = content, blog=post)
        comment.save()
    return render(request, "blog_comments.html", {'post':post, 'comments':comments})

def delete_blog_post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts':posts})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(título__contains=searched)  # Cambiado de title a título
        return render(request, "search.html", {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "search.html", {})

@login_required(login_url = '/login')
def add_blogs(request):
    if request.method=="POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.autor = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html",{'obj':obj, 'alert':alert})
    else:
        form=BlogPostForm()
    return render(request, "add_blogs.html", {'form':form})

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['título', 'slug', 'content', 'image']


def user_profile(request, myid):
    post = BlogPost.objects.filter(id=myid)
    return render(request, "user_profile.html", {'post':post})

def profile_view(request):
    profile = request.user.profile
    return render(request, 'profile.html') #se le agregaba antes ---> {'profile': profile})

def edit_profile(request):
    try:
        profile = request.user.profile  # Accede al perfil del usuario actual
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)  # Si no existe el perfil, créalo

    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado con éxito.")
            # Redirigir a la página de perfil o donde desees después de actualizar
            return redirect('profile')  # Aquí rediriges a la página de perfil del usuario
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, "edit_profile.html", {'form': form})



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        print("Usuario:", username)
        print("Contraseñas coinciden:", password1 == password2)

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password1)
        user.save()
        messages.success(request, "Usuario registrado con éxito.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect("/")  # Redirige a la página principal
        else:
            messages.error(request, "Credenciales inválidas. Inténtalo de nuevo.")
            return redirect('/login')

    return render(request, "login.html")

'''def logout(request):
    auth_logout(request)  # Cierra la sesión del usuario
    messages.success(request, "Cerró sesión exitosamente")
    return render(request, 'logout.html')  # Renderiza la página logout.html'''

def logout_and_redirect(request):
    logout(request)
    messages.success(request, "Cerraste sesión exitosamente.")
    return redirect('logout.html')  # Cambia esto por la URL a la que quieras redirigir

'''def logout_and_redirect(request):
    logout(request)
    return redirect('logout.html')'''