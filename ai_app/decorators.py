from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from admin_app.profiles import UserProfile

def status_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects(user_id=user.id).first()
        if profile and profile.status:
            return view_func(request, *args, **kwargs)
        else:
            # 如果status是False，重定向或錯誤頁
            return redirect('/ai/blocked_page/')  # 自行設定
    return _wrapped_view
