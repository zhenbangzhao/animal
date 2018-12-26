# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .petForms import petForm
from . import models
from django.shortcuts import render, redirect
from .petForms import weekForm
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def petlist(request):
    pets = models.pet.objects.all()
    paginator = Paginator(pets, 3)
    page = request.GET.get('page')
    # currentPage = int(page)

    try:
        pets = paginator.page(page)
    except PageNotAnInteger:
        pets = paginator.page(1)
    except EmptyPage:
        pets = paginator.page(paginator.num_pages)

    return render(request, 'petlist.html', locals())


def addPet(request):
    if request.method == 'GET':
        petform = petForm.PetInfo()
        return render(request, 'addpet.html', {'form': petform})
    elif request.method == 'POST':
        petform = petForm.PetInfo(request.POST)
        if petform.is_valid():
            data = petform.cleaned_data
            newPet = models.pet()
            newPet.petName = data['petName']
            newPet.petId = data['petId']
            newPet.gender = data['gender']
            newPet.year = data['year']
            newPet.kind = data['kind']
            newPet.save()
            return redirect(reverse('petlist'))
        else:
            return render(request, 'addpet.html', {'form': petform})


def editPet(request):
    if request.method == 'GET':
        id = request.GET.get('id', 0)
        pets = models.pet.objects.get(pk=int(id))
        petform = petForm.petInfo(
            initial={
                'petName': pets.petName,
                'petId': pets.petId,
                'gender': pets.gender,
                'year': pets.year,
                'kind': pets.kind,
            }             # 给需要修改的宠物添加初始属性
        )
        return render(request, 'editpet.html', {'pet': petform, 'id': id})

    elif request.method == 'POST':
        petform = petForm.petInfo(request.POST)
        id = request.POST['id']
        if petform.is_valid():
            data = petform.cleaned_data
            oldPet = models.pet.objects.get(pk=int(id))

            oldPet.petName = data['petName']
            oldPet.petId = data['petId']
            oldPet.gender = data['gender']
            oldPet.year = data['year']
            oldPet.kind = data['kind']
            oldPet.save()
            return redirect(reverse('petlist'))  # 重定向
        else:
            pet = models.pet.objects.get(pk=int(id))
            return render(request, 'editpet.html', {'pet': petform, 'id': id})


def petsin(request):
    Pets = pet.objects.all()
    id = request.GET['id']
    new = models.pet.objects.get(pk=int(id))
    values = {
        'petName': new.petName,
        'petId': new.petId,
        'gender': new.gender,
        'year': new.year,
        'kind': new.kind,

    }
    return render(request, 'pet.html', {'values': values, })


def delpet(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        pets = models.pet.objects.get(pk=int(id))
        pets.save()
        pets = models.pet.objects.all().filter(isDelete=True)
        return render(request, 'petlist.html', {'pets': pets})


def register(request):
    if request.method == 'GET':
        form = weekForm.register()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = weekForm.register(request.POST)
        if form.is_valid():
            temp = UserModel.objects.filter(userName=form.cleaned_data['userName']).exists()

            if temp == False:
                userModel = UserModel()
                userModel.userName = form.cleaned_data['userName']
                userModel.password = form.cleaned_data['password']

                userModel.save()
                return HttpResponse('数据提交成功!您可以登录了.')
            else:
                error = '用户名已经存在!'
                return render(request, 'register.html', {'form': form, 'error': error})

        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        loginform = weekForm.login()
        return render(request, 'login.html', {'form': loginform})
    elif request.method == 'POST':
        loginform = weekForm.login(request.POST)
        if loginform.is_valid():
            userName = loginform.cleaned_data['userName']
            password = loginform.cleaned_data['password']

            user = UserModel.objects.filter(userName=userName, password=password)
            if user:

                obj = UserModel.objects.get(userName=userName)
                request.session['id'] = obj.id
                request.session['username'] = obj.userName
                return render(request, 'loginsuc.html')
            else:
                error = '用户名或者密码输入有误.'
                return render(request, 'login.html', {'form': loginform, 'error': error})
        else:
            return render(request, 'login.html', {'form': loginform})
    else:
        return redirect('https://www.zhihu.com/')
