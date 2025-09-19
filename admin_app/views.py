from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate

from .decorators import unauthenticated_user_only
from .forms import SignUpForm
from .profiles import UserProfile
from ai_app.models import Order

# Create your views here.
@unauthenticated_user_only
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # 儲存User模型
            user = form.save()

            # 取出額外欄位
            name = form.cleaned_data.get('name')
            address = form.cleaned_data.get('address')

            # 建立並儲存使用者Profile（MongoDB）
            profile = UserProfile(user_id=user.id, name=name, address=address, points=0)
            profile.save()

            # 透過 authenticate 登入
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("perfume_app:index")
            else:
                form.add_error(None, "Authentication failed after sign up. Please login manually.")
    else:
        form = SignUpForm()

    return render(request, 'admin_app/signup.html', {'form': form})

def profile(request):

    orders = Order.objects.filter(user=request.user)

    profile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'orders': orders,
        'profile':profile,
    }
    return render(request, 'admin_app/profile.html', context)
