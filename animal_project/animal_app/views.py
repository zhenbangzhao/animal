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
from django.core.mail import send_mail

import xlwt
from io import StringIO, BytesIO

import logging


def petlist(request):
    pets = models.pet.objects.all()
    # paginator = Paginator(pets, 3)
    # page = request.GET.get('page')
    # currentPage = int(page)

    # try:
        # pets = paginator.page(page)
    # except PageNotAnInteger:
        # pets = paginator.page(1)
    # except EmptyPage:
        # pets = paginator.page(paginator.num_pages)

    # return render(request, 'petlist.html', locals())
    return render(request, 'petlist.html', {'pets': pets})


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
            }
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


def delpet(request, id):
    if request.method == 'GET':
        # id = request.GET.get('id')
        logger = logging.getLogger("django")
        logger.info("id=====" + id)
        # 删除
        try:
            res = models.pet.objects.filter(id=id).delete()
        # return render(request, 'petlist.html', {'pets': pets})
        except:
            return HttpResponse(res)
        return render(reverse('petlist'))


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


def output(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=user.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet(u'宠物表单')
    #1st line
    sheet.write(0, 0, 'ID')
    sheet.write(0, 1, 'petName')
    sheet.write(0, 2, 'pId')
    sheet.write(0, 3, 'gender')
    sheet.write(0, 4, 'year')
    sheet.write(0, 5, 'kind')

    data = models.pet.objects.all()
    excel_row = 1
    for item in data:
        id = item.id
        petName = item.petName
        petId = item.petId
        gender = item.gender
        year = item.year
        kind = item.kind
        sheet.write(excel_row, 0, id)
        sheet.write(excel_row, 1, petName)
        sheet.write(excel_row, 2, petId)
        sheet.write(excel_row, 3, gender)
        sheet.write(excel_row, 4, year)
        sheet.write(excel_row, 5, kind)
        excel_row += 1

    wb.save('pet.xls')
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response


def down(request):
    return render(request, 'download.html')

