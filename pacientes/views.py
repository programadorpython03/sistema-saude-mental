from django.shortcuts import render, redirect
from .models import Pacientes, Tarefas, Consultas, Visualizacoes
from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse, Http404
# Create your views here..

# Pacientes 
def pacientes(request):
    if request.method == 'GET':
        pacientes = Pacientes.objects.all()
        return render(request, 'pacientes.html', {'pacientes': pacientes, 'queixas': Pacientes.queixas_choices})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        foto = request.FILES.get('foto')
        queixa = request.POST.get('queixa')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or not foto:
            messages.add_message(request, constants.ERROR , 'Todos os campos são obrigatórios')
            return redirect('pacientes')

        paciente = Pacientes(
            nome=nome,
            email=email,
            telefone=telefone,
            foto=foto,
            queixa_principal=queixa
            )
        
        paciente.save()
        messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso')
        return redirect('pacientes')
    
# Paciente_view
def paciente_view(request, id):
    paciente = Pacientes.objects.get(id=id)

    if request.method == 'GET':
        tarefas = Tarefas.objects.all()
        consultas = Consultas.objects.filter(paciente=paciente)

        tuple_grafico = ([str(consulta.data) for consulta in consultas], [str(consulta.humor) for consulta in consultas])
        # consultas_list = []
        # for consulta in consultas:
        #     consultas_list.append(str(consulta.data))
        
        # humor_list = []
        # for consulta in consultas:
        #     humor_list.append(consulta.humor)

        # tuple_grafico = (consultas_list, humor_list)

        total_visualizacoes = Visualizacoes.objects.filter(consulta__in=consultas).count()
        total_consultas = consultas.count()

        return render(request, 'paciente.html', {'paciente': paciente, 'tarefas': tarefas, 'consultas': consultas, 'tuple_grafico': tuple_grafico, 'total_visualizacoes': total_visualizacoes, 'total_consultas': total_consultas})
    
    elif request.method == 'POST':
        humor = request.POST.get('humor')
        registro_geral = request.POST.get('registro_geral')
        video = request.FILES.get('video')
        tarefas = request.POST.getlist('tarefas')

        if not humor or not registro_geral or not video:
            messages.add_message(request, constants.ERROR, 'Todos os campos são obrigatórios')
            return redirect('paciente_view', id=id)

        consulta = Consultas(
            humor=int(humor),
            registro_geral=registro_geral,
            video=video,
            paciente=paciente
        )

        consulta.save()
        consulta.tarefas.set(tarefas)
        consulta.save()
        messages.add_message(request, constants.SUCCESS, 'Consulta cadastrada com sucesso')
        return redirect('paciente_view', id=id) 

# Atualizar Paciente
def atualizar_paciente(request, id):
    paciente = Pacientes.objects.get(id=id)
    pagamento_em_dia = request.POST.get('pagamento_em_dia')

    status = True if pagamento_em_dia == 'ativo' else False

    paciente.pagamento_em_dia = status

    paciente.save()
    
    return redirect('paciente_view', id=id)

# Excluir consulta
def excluir_consulta(request, id):
    consulta = Consultas.objects.get(id=id)
    consulta.delete()
    return redirect('paciente_view', id=consulta.paciente.id)

# Consulta pública
def consulta_publica(request, id):
    consulta = Consultas.objects.get(id=id)

    if not consulta.link_publico:
        raise Http404('Consulta não encontrada')

    if not consulta.paciente.pagamento_em_dia:
        raise Http404('Paciente não está ativo')

    return render(request, 'consulta_publica.html', {'consulta': consulta})

def registrar_visualizacao(request, id):
    consulta = Consultas.objects.get(id=id)
    ip = request.META.get('REMOTE_ADDR')
    Visualizacoes.objects.create(consulta=consulta, ip=ip)
    return redirect('consulta_publica', id=id)
