from .decorators import status_required
from django.shortcuts import render,get_object_or_404
from perfume_app.models import Perfumes
from.models import Order
from admin_app.profiles import UserProfile

import requests
import ast
from dotenv import load_dotenv
import os

load_dotenv()
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

# Create your views here.
@status_required
def question(request):
    return render(request,'ai_app/question.html')

def query_perplexity_api(questions):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": questions},
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Status code:", response.status_code)
    print("Response content:", response.text)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

@status_required
def result(request):
    if request.method == "POST":
        gender = request.POST.get('gender')
        time_choices = request.POST.getlist('time[]')
        seasons = request.POST.getlist('season[]')
        longevity = request.POST.get('longevity')
        sillage = request.POST.get('sillage')


        create_question = f'請在fragrantica.com去尋找以下牌子裹(不分次序):Chanel,Christian Dior,Creed,Diptyque,Frederic Malle,Hermes,Jo Malone,Le Labo,Maison Martin Margiela,Parfums de Marly,Tom Ford,Yves Saint Laurent而且適合以下條件的香水: {gender},{",".join(time_choices)},{",".join(seasons)},longevity:{longevity},sillage:{sillage},請選出3款評價好的香水,請將香水名子(牌子名不要)放入selected_names = [ ], 其他文字都不要'

        api_response = query_perplexity_api(create_question)

        try:
            selected_names = ast.literal_eval(api_response.split('=')[1].strip())  # 轉成Python list
        except Exception:
            selected_names = []

        p = Perfumes.objects.filter(name__in=selected_names)

        context = {
            'perfumes': p,
            'api_response':api_response,
        }
        return render(request, 'ai_app/result.html', context)

@status_required
def confirm(request):

    perfume_id = request.GET.get('perfume_id')

    perfume = get_object_or_404(Perfumes, pk=perfume_id)

    try:
        user = request.user
        profile = UserProfile.objects.get(user_id=user.id)
        address = profile.address
        name = profile.name
    except UserProfile.DoesNotExist:
        address = ''
        name = ''

    context = {
        'perfume': perfume,
        'address': address,
        'name': name,

    }
    return render(request, 'ai_app/confirm.html', context)

@status_required
def order(request):
    if request.method == "POST":
        perfume_name = request.POST.get("perfume_name")
        perfume_brand = request.POST.get("perfume_brand")
        svg_value = request.POST.get("svg_value")
        name = request.POST.get("name")
        address = request.POST.get("address")

        # 建立訂單
        Order.objects.create(
            user=request.user,
            perfume_name=perfume_name,
            perfume_brand=perfume_brand,
            svg_value=svg_value,
            address=address,
        )

        # 更新資料
        profile = UserProfile.objects.get(user_id=request.user.id)
        if profile:
            profile.name = name
            profile.address = address
            profile.status = False
            profile.save()
        else:
            # 如果不存在可建立
            UserProfile(user_id=request.user.id, name=name, address=address,point=0,status=False).save()


        return render(request, "ai_app/order.html")

def blocked_page(request):
    return render(request,'ai_app/blocked_page.html')