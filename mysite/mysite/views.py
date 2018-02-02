from django.http import HttpResponse
import datetime
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
    html = '<html><body>It is now {}.</body></html>'.format(now)
    return HttpResponse(html)
