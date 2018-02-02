"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import hello, current_datetime, hours_ahead

"""
약결합은 부분 조각을 상호 교환할 수 있게 만드는 것이 의미가 있다는 것을 나타내는 소프트웨어 개발 접근법이다.
조각 중 하나의 변경 사항은 다른 조각에 거의 영향을 미치지 않는다.
current_datetime에 대해서 2개의 URL을 사용하는 것이 약결합의 예 다.
"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello),
    path('time/', current_datetime),
    path('another-time-page/', current_datetime),
    path(r'time/plus/<int:offset>/', hours_ahead)
]
