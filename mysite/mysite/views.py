from django.http import HttpResponse, Http404
import datetime

from django.template import Context
from django.template.loader import get_template

'''
http://127.0.0.1:8000/hello 를 방문해 Hello World 메시지를 볼 때
장고는 어떻게 작동 할까?
python manage.py runserver를 실행하면 스크립트 내부 mysite 디렉터리의
settings.py 파일을 찾는다 이 파일은 특정한 장고 프로젝트를 위한 모든 종류의 설정을 포함하고 있다.
가장 중요한 설정은 ROOT_URLCONF다. ROOT_URLCOFN는 장고에게 이 웹사이트의 URLconf로 어떤 파이썬 모듈을
사용해야 하는지 알려준다.

ROOT_URLCONF = 'mysite.urls'
이것은 mysite/urls.py 파일에 해당한다. 특정 URL, 즉 /hello/-Django에 대한 요청이 들어오면
ROOT_URLCONF 설정이 가리키는 URLconf가 로드된다. 그런 다음, URLconf의 각 URL 패턴을 순서대로
검사해 일치하는 URL을 찾을 때까지 요청된 URL을 한 번에 하나씩 패턴과 비교한다.
일치하는 패턴을 찾으면 패턴과 연관된 뷰 함수를 호출해 첫 번쨰 매개변수로 HttpRequest 객체를 전달한다.
첫 번쨰 뷰 예제에서 살펴봤듯이 뷰 함수는 HttpResponse를 리턴해야 한다

1. 하나의 요청이 /hello/에 온다.
2. 장고는 ROOT_URLCONF 설정을 보고 루트 URLconf를 결정한다.
3. 장고는 /hello/와 일치하는 첫 번쨰 패턴을 찾기 위해 URLconf의 모든 URL 패턴을 찾는다.
4. 일치하는 것을 찾으면 관련 뷰 함수를 호출한다.
5. view 함수는 HttpResponse를 반환한다.
6. 장고는 HttpResponse를 적절한 HTTP 응답으로 변환해 웹 페이지를 만든다
'''


def hello(request):
    return HttpResponse('Hello World')


def current_datetime(request):
    now = datetime.datetime.now()
    """
    get_template 어떻게 템플릿을 찾는지 보자
    
    - APP_DIRS가 True로 설정돼 있고, DTL을 사용 중이라고 가정하면 현재 앱에서 템플릿 디렉터리를 찾는다
    
    - 현재 응용 프로그램에서 템플릿을 찾지 못하면 get_template()은 DIRS의 템플릿 디렉터리를 get_template()에
    전달한 템플릿 이름과 결합하고 템플릿을 찾을 때까지 각 단계를 순서대로 수행한다. 예를 들어, DIRS의 첫 번쨰 항목이
    '/hoem/django/mysite/templates'로 설정된 경우, 위의 get_template() 호출은 /home/django/mysite/
    template/current_datetime.html 템플릿을 찾는다.
    
    - get_template() 가 지정된 이름의 템플릿을 찾을 수 없으면 TemplateDoesNotExist 예외가 발생한다.
    """
    t = get_template('current_datetime.html')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)


def hours_ahead(request, offset):
    try:
        int(offset)
    except ValueError:
        raise Http404
    assert False
    time = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = '<html><body>In {} hours(s), it will be{}</body></html>'.format(offset, time)
    return HttpResponse(html)
