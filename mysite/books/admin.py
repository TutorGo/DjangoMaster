from django.contrib import admin
from .models import Publisher, Author, Book


# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    # first_name, last_name 으로 검색할 수 있는 검색 창 생성
    search_fields = ('first_name', 'last_name')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    # 변경 목록 웹페이지의 오른쪽에 필터를 만드는 데 사용할 필드의 튜플로 설정된 list_filter를 사용했다.
    # 날짜 필드의 경우, 장고는 목록을 오늘 지난 7일 이번 달 및 올해로 필터링하는 바로 가기를 제공한다
    list_filter = ('publication_date',)
    # 변경 목록 웹 페이지의 목록 상단에 날짜 드릴 다운 탐색 모음이 나타난다.
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    # 필드의 순서를 사용자 정의하라. 기본적으로 편집 양식의 필드 순서는 모델에서 정의된 순서와 일치한다
    # 우리는 ModelAdmin 하위 클래스의 fields 옵션을 사용해 변경할 수 있다.
    #fields = ('title', 'authors', 'publisher', 'publication_date')

    # 만약 publication_date 가 자동적으로 오늘로 설정된다면 fields 에서 뺴도 된다
    # fields = ('authors', 'title', 'publisher')

    # 10개 이상의 항목이 있는 ManyToManyField에 대해서는 filter_horizontal을 사용하는 것이 좋다
    # 단순한 다중 선택 위젯보다 사용하기가 훨씬 쉽다.
    # 이것은 ManyToManyField 필드에서만 작동한다.
    filter_horizontal = ('authors',)

    # 만약 수천개의 출판사가 포함되도록 book 데이터베이스가 커지면 <select> 상자에 표시하기 위해 모든
    # 출판사를 로드해야 하기 때문에 Add book 야식을 로드하는데 시간이 걸릴 수 있다

    # 이 문제를 해결하는 방법은 raw_id_fields라는 옵션을 사용 하자
    # 그럼 select 대신 간단한 텍스트 입력 상자가 나타난다
    raw_id_fields = ('publisher',)

admin.site.register(Publisher)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
