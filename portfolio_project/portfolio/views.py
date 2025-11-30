from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Projeto, Perfil, User
from .forms import ProjetoForm, PerfilForm, UserForm

# Create your views here.

# View para listar todos os projetos
def listar_projetos(request):
    projetos = Projeto.objects.all()
    return render(request, 'portfolio/projetos.html', {'projetos': projetos})

# View para criar um novo projeto (requer login)
@login_required
def criar_projeto(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES)

        if form.is_valid():
            projeto = form.save(commit=False)
            projeto.usuario = request.user
            projeto.save()
            messages.success(request, "Projeto criado com sucesso!")
            return redirect('listar_projetos')
    else:
        form = ProjetoForm()

    return render(request, 'portfolio/projetos_form.html', {'form': form})

# View para editar um projeto existente (requer login)
@login_required
def editar_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)

    # Verifica se o projeto pertence ao usuário logado
    if projeto.usuario != request.user:
        messages.warning(request, "Você não tem permissão para editar esse projeto.")
        return redirect('listar_projetos')

    if request.method == 'POST':
        form = ProjetoForm(request.POST, request.FILES, instance=projeto)
        if form.is_valid():
            form.save()
            messages.success(request, "Projeto atualizado com sucesso!")
            return redirect('listar_projetos')
    else:
        form = ProjetoForm(instance=projeto)

    return render(request, 'portfolio/projetos_form.html', {'form': form})

# View para excluir um projeto existente (requer login)
@login_required
def excluir_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)

    # Verifica se o projeto pertence ao usuário logado
    if projeto.usuario != request.user:
        messages.warning(request, "Você não tem permissão para excluir este projeto.")
        return redirect('listar_projetos')

    projeto.delete()
    messages.success(request, "Projeto excluído com sucesso!")
    return redirect('listar_projetos')

# View para exibir o perfil público de um usuário
def perfil_publico(request, username):
    usuario = get_object_or_404(User, username=username)
    perfil, created = Perfil.objects.get_or_create(usuario=usuario)
    projetos = Projeto.objects.filter(usuario=perfil.usuario)

    return render(request, 'portfolio/perfil.html', {
        'perfil': perfil,
        'projetos': projetos
    })

# View para editar o perfil do usuário (requer login)
@login_required
def editar_perfil(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil_publico', username=request.user.username)
    else:
        user_form = UserForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'portfolio/form.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'perfil': perfil
    })

# View para cadastro de novos usuários
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect('login')  # redireciona para login após cadastro
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

# View para detalhes de um projeto
def detalhe_projeto(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    return render(request, 'portfolio/detalhe_projeto.html', {'projeto': projeto})

# View para a página "sobre.html"
def sobre(request):
    return render(request, 'portfolio/sobre.html')
