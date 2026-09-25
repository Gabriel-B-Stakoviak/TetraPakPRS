from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, View
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime, time

from .models import FechamentoTurno, Extrusoura, AguaExtrusoura

class Home(TemplateView):
    template_name = 'prs_page/home.html'

    def get_context_data(self, **kwargs):
        contagem = super().get_context_data(**kwargs)
        ano_atual = timezone.now().year

        # Resumo agrupado por RE (ano atual)
        resumo_de_fardos = (
            FechamentoTurno.objects
            .filter(data__year=ano_atual)
            .values('re')
            .annotate(
                total_fardos=Sum('fardo_total'),
                total_reversao=Sum('reversao')
            )
            .order_by('re')
        )

        # Totais por turno (ano atual)
        totais_turno = (
            FechamentoTurno.objects
            .filter(data__year=ano_atual)
            .values('turno')
            .annotate(
                reversao_total=Sum('reversao'),
                fardos_totais=Sum('fardo_total')
            )
            .order_by('turno')
        )

        # Criar dicionários separados
        totais_fardos = {item['turno']: item['fardos_totais'] for item in totais_turno}
        totais_reversao = {item['turno']: item['reversao_total'] for item in totais_turno}

        # Adicionar valores individuais
        contagem['turno_a_total'] = totais_fardos.get('A', 0)
        contagem['turno_b_total'] = totais_fardos.get('B', 0)
        contagem['turno_c_total'] = totais_fardos.get('C', 0)

        contagem['reversao_a_total'] = totais_reversao.get('A', 0)
        contagem['reversao_b_total'] = totais_reversao.get('B', 0)
        contagem['reversao_c_total'] = totais_reversao.get('C', 0)

        # Totais gerais (ano atual)
        contagem['total_geral'] = (
            FechamentoTurno.objects
            .filter(data__year=ano_atual)
            .aggregate(total=Sum('fardo_total'))['total'] or 0
        )
        contagem['total_reversao_geral'] = (
            FechamentoTurno.objects
            .filter(data__year=ano_atual)
            .aggregate(total=Sum('reversao'))['total'] or 0
        )

        contagem['resumo_de_fardos'] = resumo_de_fardos
        contagem['totais_turno_fardos'] = totais_turno
        contagem['ano_atual'] = ano_atual

        return contagem

class ExtrusouraList(ListView):
    template_name = 'prs_page/extrusoura.html'
    model = Extrusoura
    context_object_name = 'extrusoura_list'

    def get_queryset(self):
        ano_atual = timezone.now().year
        return Extrusoura.objects.filter(data__year=ano_atual)

class ExtrusouraCreate(CreateView):
    model = Extrusoura
    template_name = 'prs_page/extrusoura_form.html'
    fields = ['re', 'maquina_rodando', 'maquina_disponivel', 'detalhamento']
    success_url = reverse_lazy('extrusoura')

    def form_valid(self, form):
        hora_atual = datetime.now().strftime('%H:%M')

        if hora_atual >= time(6, 15).strftime("%H:%M") and hora_atual < time(14, 20).strftime("%H:%M"):
            turno = 'A'
        elif hora_atual >= time(14, 21).strftime("%H:%M") and hora_atual < time(22, 25).strftime("%H:%M"):
            turno = 'B'
        else:
            turno = 'C'

        form.instance.turno = turno
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        marcadores = super().get_context_data(**kwargs)
        marcadores['horario'] = datetime.now().strftime('%H:%M')
        marcadores['data'] = datetime.now().strftime('%d/%m/%Y')
        return marcadores

class ExtrusouraViewFim(View):
    def get(self, request, pk):
        extrusoura = get_object_or_404(Extrusoura, pk=pk)
        extrusoura.fim = datetime.now().strftime('%H:%M')
        extrusoura.save()
        return redirect('extrusoura')

class AguaExtrusouraList(ListView):
    template_name = 'prs_page/agua_extrusoura.html'
    model = AguaExtrusoura
    context_object_name = 'agua_extrusoura_list'

    def get_queryset(self):
        ano_atual = timezone.now().year
        return AguaExtrusoura.objects.filter(data__year=ano_atual)

class AguaExtrusouraCreate(CreateView):
    model = AguaExtrusoura
    template_name = 'prs_page/agua_extrusoura_form.html'
    fields = ['re', 'cloro', 'turbidez', 'observacao']
    success_url = reverse_lazy('agua_extrusoura')

    def form_valid(self, form):
        hora_atual = datetime.now().strftime('%H:%M')

        if hora_atual >= time(6, 15).strftime("%H:%M") and hora_atual < time(14, 20).strftime("%H:%M"):
            turno = 'A'
        elif hora_atual >= time(14, 21).strftime("%H:%M") and hora_atual < time(22, 25).strftime("%H:%M"):
            turno = 'B'
        else:
            turno = 'C'

        form.instance.turno = turno
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        marcadores = super().get_context_data(**kwargs)
        marcadores['horario'] = datetime.now().strftime('%H:%M')
        marcadores['data'] = datetime.now().strftime('%d/%m/%Y')
        return marcadores

class FechamentoTurnoPage(ListView):
    template_name = 'prs_page/fechamento_turno.html'
    model=FechamentoTurno
    context_object_name='fechamento_turno_list'

    def get_queryset(self):
        ano_atual = timezone.now().year
        return FechamentoTurno.objects.filter(data__year=ano_atual)
    
class FechamentoTurnoCreate(CreateView):
    model=FechamentoTurno
    template_name = 'prs_page/fechamento_turno_form.html'
    fields = ['re', 'fardo_virgem', 'fardo_laminado', 'reversao', 'observacao']
    success_url = reverse_lazy('fechamento_turno')
    
    def form_valid(self, form):
        hora_atual = datetime.now().strftime('%H:%M')

        if hora_atual >= time(6, 15).strftime("%H:%M") and hora_atual < time(14, 20).strftime("%H:%M"):
            turno = 'A'
        elif hora_atual >= time(14, 21).strftime("%H:%M") and hora_atual < time(22, 25).strftime("%H:%M"):
            turno = 'B'
        else:
            turno = 'C'

        form.instance.turno = turno
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        marcadores = super().get_context_data(**kwargs)
        marcadores['horario'] = datetime.now().strftime('%H:%M')
        marcadores['data'] = datetime.now().strftime('%d/%m/%Y')
        return marcadores
