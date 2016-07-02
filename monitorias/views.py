from django.shortcuts import render, get_object_or_404
from monitorias.models import SeccionMonitoria, AffiliateCompany, RecommendedTools
from monitorias.forms import SeccionMonitoriaForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from postman.api import pm_write
# Create your views here.

def secciones_list(request):
    # import ipdb
    # ipdb.set_trace()
    secciones = []
    pendiente = "pendiente"
    aceptada = "aceptada"
    rechazada = "rechazada"
    # integrales = SeccionMonitoria.objects.filter(subject__name="Calculo Integral")
    # integralesSubject = integrales[0].subject
    for i in SeccionMonitoria.objects.all().order_by('-publish_date'):
        if request.user.userprofile.isTutor:
            if i.estudiante == request.user or i.tutor == request.user:
                    secciones.append(i)
        else:
            if i.estudiante == request.user:
                secciones.append(i)

    return render(request, 'monitorias/secciones_list.html', {'secciones': secciones, 'pendiente': pendiente, 'aceptada': aceptada, 'rechazada': rechazada})

# Funcion para filtrar lista de secciones de monitorias agendadas

def secciones_list_estado(request, estado):

    secciones = []

    for i in SeccionMonitoria.objects.all().order_by('-publish_date'):
        if request.user.userprofile.isTutor:
            if (i.estudiante == request.user or i.tutor == request.user) and \
                    (i.status == "pendiente" and estado == "1"):
                secciones.append(i)

            if (i.estudiante == request.user or i.tutor == request.user) and \
                    (i.status == "aceptada" and estado == "2"):
                secciones.append(i)

            if (i.estudiante == request.user or i.tutor == request.user) and \
                    (i.status == "rechazada" and estado == "3"):
                secciones.append(i)
        else:
            if (i.estudiante == request.user) and (i.status == "pendiente" and estado == "1"):
                secciones.append(i)

            if (i.estudiante == request.user) and (i.status == "aceptada" and estado == "2"):
                secciones.append(i)

            if (i.estudiante == request.user) and (i.status == "rechazada" and estado == "3"):
                secciones.append(i)

    return render(request, 'monitorias/secciones_list.html', {'secciones': secciones})


def secciones_detail(request,pk):
    seccion = get_object_or_404(SeccionMonitoria, pk=pk)
    return render(request, 'monitorias/secciones_detail.html', {'seccion': seccion})

def secciones_new(request, tutorpk):
    tutor = User.objects.get(pk=tutorpk)
    admin = User.objects.get(username="quicktutors")
    if request.method == "POST":
        form = SeccionMonitoriaForm(request.POST)
        if form.is_valid():
            seccion = form.save(commit=False)
            seccion.estudiante = request.user
            seccion.tutor = tutor

            pm_write(admin, tutor, "Nueva Solicitud de monitoria.",
                     "Hola " + tutor.get_short_name() + ",\n\n Tienes una"
                                                        " nueva solicitud"
                                                        " pendiente en tu lista"
                                                        " de monitorias.\n\n"
                                                        "Estudiante: " +
                     seccion.estudiante.get_full_name() + "\nMateria: " + seccion.subject.name + "\n\n-Quicktutors Staff.")

            if seccion.payment_method == "online":
                seccion.seccion_payed = True
                seccion.save()
                return redirect('/secciones/online_payment/')
            else:
                seccion.seccion_payed = False
                seccion.save()
                return redirect('/secciones/onsite_payment')

    else:
        form = SeccionMonitoriaForm()
    return render(request, 'monitorias/secciones_new.html', {'form': form, 'tutor': tutor})

# view para que un tutor pueda aceptar una seccion de monitoria
def secciones_aceptar(request, pk):
    seccion = SeccionMonitoria.objects.get(pk=pk)
    seccion.status = "aceptada"
    seccion.save()
    # Enviar mensaje al estudiante con el mensaje de que ha sido rechazada la solicitud
    pm_write(seccion.tutor, seccion.estudiante,
             "Tu seccion de monitoria para la materia " + seccion.subject.name + "ha sido aceptada.",
             "Hola " + seccion.estudiante.get_short_name() + ",\n\n Me complace informarte que estoy disponible"
                                                             " para impartirte tu seccion de monitoria, y me parece bien"
                                                             " el horario seleccionado, asi como lugar de encuentro, estaremos en"
                                                             " contacto por esta via para una futura confirmacion de la"
                                                             " cita.\n\n" \
                                                             "Gracias por utilizar nuestro servicio,\n\n" \
                                                             "-" + seccion.tutor.get_short_name())
    return redirect('/secciones/')

# view para que un tutor pueda rechazar una seccion de monitoria
def secciones_rechazar(request, pk):
    seccion = SeccionMonitoria.objects.get(pk=pk)
    seccion.status = "rechazada"
    seccion.save()
    # Enviar mensaje al estudiante con el mensaje de que ha sido rechazada la solicitud
    pm_write(seccion.tutor, seccion.estudiante,
             "Tu seccion de monitoria para la materia " + seccion.subject.name + "ha sido rechazada.",
             "Hola " + seccion.estudiante.get_short_name() +",\n\n Lamento informarte que no podre impartirte" \
                                                           " la seccion de monitoria solicitada ya que no estare" \
                                                           " disponible en ese horario. pero espero que en un futuro" \
                                                           " podamos estudiar juntos!\n\n" \
                                                           "Gracias por utilizar nuestro servicio,\n\n" \
                                                           "-" + seccion.tutor.get_short_name())

    return redirect('/secciones/')


def secciones_new_accepted(request):
    return render(request, 'monitorias/accepted.html')


def secciones_new_cancelled(request):
    return render(request, 'monitorias/cancelled.html')


def secciones_online_payment(request):
    return render(request, 'monitorias/online_payment_page.html')


def secciones_onsite_payment(request):
    affiliates_list = AffiliateCompany.objects.all()
    return render(request, 'monitorias/onsite_payment_page.html', {'affiliates_list': affiliates_list})

def secciones_recommended_tools(request):
    tools_list = RecommendedTools.objects.all()
    return render(request, 'monitorias/recommended_tools_page.html', {'tools_list': tools_list})
