from django.shortcuts import render
from django.contrib.auth.models import Group
from django.contrib import messages

from .forms import WaiterForm


def create_waiter(request):
    context = {}
    form = WaiterForm(request.POST or None)

    if request.method == 'POST':
        waiter_group = Group.objects.get(name='Waiter')

        if form.is_valid():
            password = form.cleaned_data['password']
            waiter = form.save()
            waiter.set_password(password)
            waiter.groups.add(waiter_group)
            waiter.is_waiter = True
            waiter.save()
            context['form'] = WaiterForm()
            messages.add_message(
                request=request, 
                level=messages.SUCCESS, 
                message='Garçon criado com sucesso!'
            )

            return render(
                request=request, 
                template_name='create_waiter.html', 
                context=context
            )
        messages.add_message(
            request=request, 
            level=messages.ERROR, 
            message='Algo deu errado ao criar Garçon!'
        )
    else:
        form = WaiterForm()

    context = {'form': form}

    return render(
        request=request, 
        template_name='create_waiter.html', 
        context=context
    )
