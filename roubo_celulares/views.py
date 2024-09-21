from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.http import HttpResponseForbidden
from .models import Roubo, Bairro, Feedback
from .forms import FeedbackForm, BairroForm


def mapa_roubos(request):
    query = request.GET.get('query', '')

    if query:
        # Filtrar dados com base na consulta do usuário e descr_tipolocal
        roubos = Roubo.objects.filter(bairro__nome__icontains=query, descr_tipolocal='Via Pública')
    else:
        # Filtrar apenas por descr_tipolocal
        roubos = Roubo.objects.filter(descr_tipolocal='Via Pública')

    # Calcular os 5 bairros mais atacados
    bairros_mais_atacados = (
        roubos.values('bairro__nome')
        .annotate(num_ocorrencias=Count('bairro'))
        .order_by('-num_ocorrencias')[:5]
    )

    # Obter coordenadas da tabela Bairro
    bairros_com_coordenadas = []
    for bairro_data in bairros_mais_atacados:
        bairro_obj = Bairro.objects.filter(nome__iexact=bairro_data['bairro__nome']).first()

        if bairro_obj:
            bairros_com_coordenadas.append({
                "id": bairro_obj.id,
                "bairro": bairro_obj.nome,
                "latitude": bairro_obj.latitude,
                "longitude": bairro_obj.longitude,
                "num_ocorrencias": bairro_data['num_ocorrencias']
            })

    context = {
        'bairros_mais_atacados': bairros_com_coordenadas,
        'query': query,
    }

    return render(request, 'filtrar_roubos.html', context)


def detalhes_ocorrencia(request, id):
    # Obtém o bairro pelo ID
    bairro = get_object_or_404(Bairro, id=id)

    # Filtra as ocorrências relacionadas ao bairro, usando diretamente o objeto `bairro`
    ocorrencias = (
        Roubo.objects.filter(bairro=bairro)
        .exclude(hora_ocorrencia='00:00:00')
        .exclude(logradouro__icontains='VEDAÇÃO DA DIVULGAÇÃO DOS DADOS RELATIVOS')
        .values('logradouro', 'hora_ocorrencia')
        .annotate(num_ocorrencias=Count('id'))
        .order_by('-num_ocorrencias')
    )

    # Agrupa as ocorrências por logradouro e horários, contando as ocorrências por hora
    ocorrencias_agrupadas = {}
    for ocorrencia in ocorrencias:
        logradouro = ocorrencia['logradouro']
        hora = ocorrencia['hora_ocorrencia'].strftime('%H:%M') if ocorrencia['hora_ocorrencia'] else 'Desconhecida'
        num_ocorrencias = ocorrencia['num_ocorrencias']

        if logradouro not in ocorrencias_agrupadas:
            ocorrencias_agrupadas[logradouro] = {'horas': {}, 'total': 0}

        if hora not in ocorrencias_agrupadas[logradouro]['horas']:
            ocorrencias_agrupadas[logradouro]['horas'][hora] = num_ocorrencias
        else:
            ocorrencias_agrupadas[logradouro]['horas'][hora] += num_ocorrencias

        ocorrencias_agrupadas[logradouro]['total'] += num_ocorrencias

    # Ordena os logradouros por número total de ocorrências de forma decrescente
    ocorrencias_agrupadas = dict(sorted(ocorrencias_agrupadas.items(), key=lambda x: x[1]['total'], reverse=True))

    # Ocorrências com horário '00:00:00' (horário manual)
    ocorrencias_sem_horario = Roubo.objects.filter(bairro=bairro, hora_ocorrencia='00:00:00').count()

    context = {
        'bairro': bairro,
        'ocorrencias_agrupadas': ocorrencias_agrupadas,
        'ocorrencias_sem_horario': ocorrencias_sem_horario,
    }

    return render(request, 'detalhes_ocorrencia.html', context)

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(
                nome=form.cleaned_data['nome'],
                email=form.cleaned_data['email'],
                experiencia=form.cleaned_data['experiencia'],
                melhorias=form.cleaned_data['melhorias'],
                # Ajuste os comentários se necessário
                comentario=form.cleaned_data.get('comentario', ''),  # Usando o 'comentario' aqui
            )
            return redirect('feedback_success')
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})



def feedback_success(request):
    return render(request, 'feedback_success.html')


# Listar todos os bairros
def listar_bairros(request):
    if request.user.is_authenticated:
        query = request.GET.get('query', '')
        if query:
            bairros = Bairro.objects.filter(nome__icontains=query)
        else:
            bairros = Bairro.objects.all()
        return render(request, 'listar_bairros.html', {'bairros': bairros, 'query': query})
    else:
        return HttpResponseForbidden("Você precisa estar autenticado e ser administrador para acessar esta página.")


# Editar um bairro
def editar_bairro(request, bairro_id):
    if request.user.is_authenticated:
        bairro = get_object_or_404(Bairro, id=bairro_id)
        print(bairro)

        if request.method == 'POST':
            form = BairroForm(request.POST, instance=bairro)
            if form.is_valid():
                form.save()
                return redirect('listar_bairros')
        else:
            form = BairroForm(instance=bairro)

        return render(request, 'editar_bairro.html', {'form': form, 'bairro': bairro})
    else:
        return HttpResponseForbidden("Você precisa estar autenticado e ser administrador para acessar esta página.")


# Deletar um bairro
def deletar_bairro(request, bairro_id):
    if request.user.is_authenticated and request.user.is_staff:
        bairro = get_object_or_404(Bairro, id=bairro_id)
        if request.method == 'POST':
            bairro.delete()
            return redirect('listar_bairros')
        return render(request, 'deletar_bairro.html', {'bairro': bairro})
    else:
        return HttpResponseForbidden("Você precisa estar autenticado e ser administrador para acessar esta página.")
