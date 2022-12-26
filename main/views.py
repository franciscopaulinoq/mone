from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from main.models import *
from main.forms import *

# Create your views here.

@login_required
def index(request, year = datetime.now().year, month = datetime.now().month):

    year_now = datetime.now().year
    month_now = datetime.now().month

    # Mudando os valores conforme o ano e mês do input no html
    if request.method == 'GET':
        if request.GET.get('ano'):
            year = request.GET.get('ano')
            year_now = request.GET.get('ano')
        if request.GET.get('mes'):
            month = request.GET.get('mes')
            month_now = request.GET.get('mes')

    # Queries para o gráfico de linhas e o gráfico de barra
    receitas = Receita.objects.values('data__month').order_by('data__month').annotate(Sum('valor')).filter(data__year = year)
    gastos = Gasto.objects.values('data__month').order_by('data__month').annotate(Sum('valor')).filter(data__year = year)

    # Queries e variáveis para o gráfico doughnut
    gastos_categorias = Gasto.objects.values('categoria').order_by('-valor').annotate(Sum('valor')).filter(data__year = year, data__month = month)
    categorias = Categoria.objects.values('nome')
    cor_categorias = Categoria.objects.values('cor')
    limit = gastos_categorias.count()
    cont = 0

    # Queries para a barra de economia
    receitas_mes = Receita.objects.values('data__month').annotate(Sum('valor')).filter(data__year = year, data__month = month)
    gastos_mes = Gasto.objects.values('data__month').annotate(Sum('valor')).filter(data__year = year, data__month = month)

    receitas_ano = '['
    gastos_ano = '['
    list_receitas = [0] * 12
    list_gastos = [0] * 12

    # For para preencher os dados das receitas no gráfico de linhas
    receita_anual = 0
    for x in range(1, 13):
        for y in receitas:
            if x == y.get('data__month'):
                if x == 12:
                    receita_anual += float(y.get('valor__sum'))
                    list_receitas[x-1] = float(y.get('valor__sum'))
                    receitas_ano += (str(y.get('valor__sum')) + ']')
                else:
                    receita_anual += float(y.get('valor__sum'))
                    list_receitas[x-1] = float(y.get('valor__sum'))
                    receitas_ano += (str(y.get('valor__sum')) + ', ')
                break
        else:
            if x == 12:
                receita_anual += float(0)
                list_receitas[x-1] = float(0)
                receitas_ano += ('0]')
            else:
                receita_anual += float(0)
                list_receitas[x-1] = float(0)
                receitas_ano += ('0, ')

    # For para preencher os dados dos gastos no gráfico de linhas
    gasto_anual = 0
    for x in range(1, 13):
        for y in gastos:
            if x == y.get('data__month'):
                if x == 12:
                    gasto_anual += float(y.get('valor__sum'))
                    list_gastos[x-1] = float(y.get('valor__sum'))
                    gastos_ano += (str(y.get('valor__sum')) + ']')
                else:
                    gasto_anual += float(y.get('valor__sum'))
                    list_gastos[x-1] = float(y.get('valor__sum'))
                    gastos_ano += (str(y.get('valor__sum')) + ', ')
                break
        else:
            if x == 12:
                gasto_anual += float(0)
                list_gastos[x-1] = float(0)
                gastos_ano += ('0]')
            else:
                gasto_anual += float(0)
                list_gastos[x-1] = float(0)
                gastos_ano += ('0, ')
    
    card_receita_anual = '{:.2f}'.format(receita_anual)
    card_gasto_anual = '{:.2f}'.format(gasto_anual)

    # For para o gráfico de barras
    saldos_ano = [0] * 12
    for x in range(0, 12):
        saldos_ano[x] = (list_receitas[x] - list_gastos[x])

    categorias_nome = [None]*limit
    categorias_cor = [None]*limit
    categorias_gastos = '['

    # For para o gráfico doughnut
    for x in gastos_categorias:
        cont += 1
        if cont == limit:
            categorias_nome[cont-1] = categorias.filter(id = x.get('categoria')).get()
            categorias_cor[cont-1] = cor_categorias.filter(id = x.get('categoria')).get()
            categorias_gastos += (str(x.get('valor__sum')) + ']')
        else:
            categorias_nome[cont-1] = categorias.filter(id = x.get('categoria')).get()
            categorias_cor[cont-1] = cor_categorias.filter(id = x.get('categoria')).get()
            categorias_gastos += (str(x.get('valor__sum')) + ', ')

    # For para os cards de receita, gasto e saldo
    card_receitas = '0.00'
    card_gastos = '0.00'
    receitas_cal = 0
    gastos_cal = 0
    for x in receitas_mes:
        receitas_cal = float(x.get('valor__sum'))
        card_receitas = '{:.2f}'.format(float(x.get('valor__sum')))
    
    for x in gastos_mes:
        gastos_cal = float(x.get('valor__sum'))
        card_gastos = '{:.2f}'.format(float(x.get('valor__sum')))
    
    card_saldo = '{:.2f}'.format(float(receitas_cal - gastos_cal))

    # Dados da barra de economia
    avalue = '0.00'
    avalue_num = 0
    porcen = 0
    porcentagem = ''
    dif = ''
    if receitas_cal == 0:
        avalue = '{:.2f}'.format(0)
        avalue_num = 0
        dif = '{:.2f}'.format(gastos_cal - receitas_cal)
    else:
        porcen = gastos_cal*100/receitas_cal
        if porcen > 100:
            avalue_num = 0
            avalue = '{:.2f}'.format(0)
            porcentagem = '{:.2f}'.format(porcen - 100)
            dif = '{:.2f}'.format(gastos_cal - receitas_cal)
        else:
            avalue = '{:.2f}'.format(100 - porcen)
            avalue_num = 100 - porcen
            porcentagem = '{:.2f}'.format(100 - porcen)
            dif = '{:.2f}'.format(receitas_cal - gastos_cal)

    bg_cor = 'bg-secondary'
    if avalue_num > 30 and avalue_num <= 100:
        bg_cor = 'bg-success'
    else:
        if avalue_num > 15 and avalue_num <= 30:
            bg_cor = 'bg-warning'
        else:
            if avalue_num >= 0 and avalue_num <= 15:
                bg_cor = 'bg-danger'
    
    context = {
        'receitas_ano' : receitas_ano,
        'gastos_ano' : gastos_ano,
        'saldos_ano' : saldos_ano,
        'categorias_nome' : categorias_nome,
        'categorias_cor' : categorias_cor,
        'categorias_gastos' : categorias_gastos,
        'card_receitas' : card_receitas,
        'card_gastos' : card_gastos,
        'card_saldo' : card_saldo,
        'card_receita_anual' : card_receita_anual,
        'card_gasto_anual' : card_gasto_anual,
        'avalue' : avalue,
        'porcen' : porcen,
        'porcentagem' : porcentagem,
        'dif' : dif,
        'bg_cor' : bg_cor,
        'year_now' : year_now,
        'month_now' : month_now,
    }
    return render(request,'index.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def categoria(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        form = CategoriaForm(request.POST) 
        if form.is_valid():
            form.save()
            form = CategoriaForm()
    else:
        form = CategoriaForm()

    context = {
        'form' : form,
        'categorias' : categorias,
    }

    return render(request,'categoria.html', context)

@login_required
def remover_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    categoria.delete()
    return redirect('categoria')

@login_required
def update_categoria(request, pk):
    categorias = Categoria.objects.all()

    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        return redirect('categoria')
    
    context = {
        'form' : form,
        'categorias' : categorias,
    }
    
    return render(request, "categoria.html", context)

@login_required
def receita(request):
    receitas = Receita.objects.all()

    if request.method == 'POST':
        form = ReceitaForm(request.POST) 
        if form.is_valid():
            form.save()
            form = ReceitaForm()
    else:
        form = ReceitaForm()

    context = {
        'form' : form,
        'receitas' : receitas,
    }

    return render(request,'receita.html', context)

@login_required
def remover_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    receita.delete()
    return redirect('receita')

@login_required
def update_receita(request, pk):
    receitas = Receita.objects.all()

    receita = get_object_or_404(Receita, pk=pk)
    form = ReceitaForm(request.POST or None, instance=receita)
    if form.is_valid():
        form.save()
        return redirect('receita')
    
    context = {
        'form' : form,
        'receitas' : receitas,
    }
    
    return render(request, "receita.html", context)

@login_required
def gasto(request):
    gastos = Gasto.objects.all()

    if request.method == 'POST':
        form = GastoForm(request.POST) 
        if form.is_valid():
            form.save()
            form = GastoForm()
    else:
        form = GastoForm()

    context = {
        'form' : form,
        'gastos' : gastos,
    }

    return render(request,'gasto.html', context)

@login_required
def remover_gasto(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    gasto.delete()
    return redirect('gasto')

@login_required
def update_gasto(request, pk):
    gastos = Gasto.objects.all()

    gasto = get_object_or_404(Gasto, pk=pk)
    form = GastoForm(request.POST or None, instance=gasto)
    if form.is_valid():
        form.save()
        return redirect('gasto')
    
    context = {
        'form' : form,
        'gastos' : gastos,
    }
    
    return render(request, "gasto.html", context)