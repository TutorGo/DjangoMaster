# Django Template



1. 템플릿 시스템이 변수 이름에서 점을 발견하면 순서대로 다음 조회를 시도한다.
	- Dicionary lookup(예: foo["bar"])
	- Attribute lookup(예: foo.bar)
	- Method call(예: foo.bar())
	- List-index lookup(예: foo[2])


## 메서드 호출

-  메서드 룩업을 하는 동안 메서드가 예외를 발생시킬 경우, 이 예외의 값이 slient\_variable\_failure = True 아니라면 예외는 전파된다.
-  예외가 slient_variable_failure 속성을 갖는다면 해당 변수는 엔진의 string\_if\_invalid 구성 옵션 값(기본적으로는 빈 문자열)으로 렌더링된다. 이에 대한 예제는 다음과 같다.

```
t = Template("My name is {{ person.first_name }}.")

class PersonClass3:
	def first_name(self):
		raise AssertionError("foo")

p = PersonClass3()
t.render(Context({"perosn": p}))

Traceback (most recent call last):
...
AssertionError: foo

class SlientAssertionError(exception):
	slient_variable_failure = True

class PersonClass4:
	def first_name(self):
		raise SillentAssertionError

p = PersonClass4()
t.render(Context({"person": p}))

'My name is .'
```

- 메서드 호출은 메서드가 필수 인수를 갖지 않는 경우에만 작동한다. 그렇지 않으면 이 시스템은 다음 룩업 유형(리스트-인덱스 룩업)으로 이동한다.
- 설계에 따라 장고는 템플릿에서 사용할 수 있는 논리 처리량을 의도적으로 제한하므로 템플릿 내에서 접근하는 메서드 호출에 인수를 전당할 수 없다. 데이터는 뷰에서 계산된 다음 화면 표시를 위해 템플릿으로 절달돼야 한다.
- 분명히 어떤 방법은 부작용이 있으며, 템플릿 시스템이 액세스할 수 있게 하는 것이 가장 좋을 뿐만 아니라 보안상의 허점일 수도 있다.
- 예를 들어, delete() 메서드가 있는 BankAcoount 객체가 있따고 가정해보자. 템플릿에 BankAccount 객체인 {{account.delete}}와 같은 것을 포함하면 템플릿이 렌더링될 떄 겍체가 삭제된다. 따라서 이를 방지하려면 메서드에 함수 속성 alters_data를 설정해야 한다.


```
def delete(self):
	delete.alters_data = True
```

- 템플릿 시스템은 이 방법으로 표시된 메서드를 실행하지 않는다. 앞의 예제에서 템플릿이 {{account.delete}}를 포함하고 delete() 메서드가 alter_data = True이면, 템플릿이 렌더링될 때 delete() 메서드가 실행되지 않고, 그 대신 엔진이 해당 변수를 string_if_invalid 으로 교체한다.
- 주의사항: 장고 모델 객체에서 동적으로 생성된 delete() 및 save() 메서드는 alter_data = true를 자동으로 설정한다.


## for

- forloop.counter는 항상 루프가 입력된 횟수를 나타내는 정수로 설정된다. 이것에는 하나의 색인이 붙어 있기 떄문에 청므으로 루프를 돌 때 forloop.counter가 1로 설정된다.
- forloop.counter0은 첫 인덱스가 0 으로 지정된다.
- forloop.revcounter는 항상 루프의 나머지 항목 수를 나타내는 정수로 설정된다. 루프를 처음 실행할 때 forloop.revcounter는 순회 중인 시퀀스의 총 항목 수로 설정된다. 루프를 마지막으로 통과하면 forloop.revcounter가 1로 설정된다.
- forloop.revcounter0은 루프를 마지막으로 거치면 0으로 설정된다.
- forloop.first는 루프를 처음 실행할 경우, 부울 값이 Ture로 설정된다.
- forloop.last는 루프를 마지막으로 통과한 경우, 부울 값이 Ture로 설정된다.

```
{% for link in links %}
	{{ link }}{% if not forloop.last %} | {% endif %}
{% endfor %}
```

위의 템플릿 코드는 다음과 같이 출력할 수 있다.

```
Link1 | Link2 | Link3 | Link4
```

일반적인 용도는 목록에서 단어 사이에 쉼표를 넣는 것이다.

```
{% for p in places %}{{ p }}{% if not forloop.last %},
	{% endif %}
{% endfor %}
```

- forloop.parentloop는 중첩 루프의 경우 부모 루프에 대한 forloop 객체에 대한 참조다

```
{% for country in countries %}
	<tables>
	{% for city in country.city_list %}
		<tr>
		<td>Country #{{ forloop.parentloop.counter }}</td>
		<td>City #{{ forloop.counter }}</td>
		<td>{{ city }}</td>
		</tr>
	{% endfor %}
	</table>
{% endfor %}
```

## ifequla / ifnotequal

- {% ifequal %} 태그는 두 값을 비교해 값이 동일하면 {% ifequal %}와 {% endifequal %} 사이의 모든 것을 표시한다. 이 예제에서는 템프릿 변수 user 및 currentuser 를 비교

```
{% ifequal user currentuser %}
	<h1>Welcome! </h1>
{% endifeuqal %}
```

- 인수는 작은 따옴표나 큰 따옴표로 하드코딩된 문자열일 수 있으므로 다음이 유효하다.

```
{% ifequal section 'sitenews' %}
	<h1>Site News</h1>
{% endifequal %}
```

- {% if %}와 같이 {% ifequal %} 테그는 선택적 {% else %}를 지원한다.

```
{% ifequal section 'sitenews' %}
	<h1>Site News</h1>
{% else %}
	<h1>No News Here</h1>
{% endifequal %}
```

- 템픔릿 변수, 문자열, 정수 및 십진수만 {% ifequal %}에 대한 인수로 사용할 수 있다.

```
{% ifequal variable 1 %}
{% ifequal variable 1.23 %}
{% ifequal variable 'foo' %}
{% ifequal variable "foo" %}
```

- 파이썬 딕셔너리, 리스트 또는 불린과 같은 다른 유형의 변수는 {% ifequal %}에 하드코드될 수 없다. 

```
{% ifequal variable True %}
{% ifequal variable [1, 2, 3] %}
{% ifequal variable {'key': 'value'} %}
```

- 뭔가가 true인지 또는 fasle인지 테스트해야하는 하는 경우, {% ifequal %} 대신 {% if %} 를 사용하자

- ifequal 태그에 대한 대안은 if 태그와 "==" 연산자를 사용하는 것이다.

## 주석

- 주석을 지정하려면 {# #}사용해야 한다.
- 여러 줄 주석을 사용하려면 {% comment %} {% endcommet %} 사용하자

## 필터

필터는 다음과 같이 파이프 문자를 사용한다.

- 텍스트를 소문자로 변환하는 하위 필터를 통해 필터링한 후 {{name}} 변수의 값을 표시한다. 필터는 연결될 수 있다. 즉, 한 필터의 출력이 다음 필터에 적용되도록 함계 사용할 수 있다.

```
{{ name|lower }}
```

다음은 리스트의 첫 번째 요소를 대문자로 변환

```
{{ my_list|first|upper }}
```

일부 필터는 인수를 사용한다. 필터 인수는 콜론(:) 뒤에 오며 항상 큰 따옴표로 묶인다.

- 이것은 바이오 변수의 처음 30개 단어를 표시한다.

```
{{ bio|truncatewords:"30" }}
```

- 다음은 가장 중요한 몇 가지 필터다
	- addslashes: 백슬래시, 작은 따옴표 또는 큰 따옴표 앞에 백슬래시를 추가한다. 이렇게 하면 이스케이프 문자열에 유용하다. 사용 예제는 다음과 같다.
	
	```
	{{ value|addslashes }}
	
	If value is "I'm using Django", the output will be "I\'m using Django"
	```
	
	- date: 매개변수에 지정된 형식 문자열에 따라 date 또는 datetime 객체를 형식화한다.
	```
	{{ pub_date|date:"F j, y" }}
	```
	

## 철학과 한계

장고는 대량으로 끊임없이 변화하는 온라인 뉴스 룸 환경에서 개발됐다. 장고의 원래 제작자는 DTL을 작성하는 데 있어 철저한 철학을 갖고 있엇다

1. 프레젠테이션에서 분리된 로직임
	- 템플릿 시스템은 프레젠테이션과 프레젠테이션 관련 로직을 제어하는 도구일뿐이다. 이 템플릿 시스템은 기본 목적을 넘어서는 기능을 지원해서는 안 된다.

2. 중복성을 고려하지 않음
	- 대다수의 동적 웹사이트는 공통된 머리글, 바닥글, 탐색 모음 등과 같은 일종의 일반적인 웹 사이트 전체 디자인을 사용한다. 장고 템플릿 시스템은 중복된 코드를 제거해 이러한 요소를 단일 위치에 쉽게 저장해야 한다. 이것이 템플릿 상속의 철학이다.

3. HTML과 분리됨
	- 템플릿 시스템은 HTML만 출력하도록 설계하면 안 된다. 다른 텍스트 기반 형식 이나 일반 텍스트를 생성할 때도 이와 똑같이 잘 맞아야 한다.

4. XML을 템플릿 언어로 사용해서는 안 됨
	- XML 엔진을 사용해 템플릿을 구문 분석하면 템플릿을 편집할 떄 완전히 새로운인적 오류가 발생할 수 있으며, 템플릿 처리에서 허용할 수 없는 수준의 오버헤드가 발생한다.
	- 오버헤드: 오버헤드는 어떤 처리를 하기 위해 들어가는 간접적인 처리 시간 · 메모리 등을 말한다. 예를 들어 A라는 처리를 단순하게 실행한다면 10초 걸리는데, 안전성을 고려하고 부가적인 B라는 처리를 추가한 결과 처리시간이 15초 걸렸다면, 오버헤드는 5초가 된다. 또한 이 처리 B를 개선해 B'라는 처리를 한 결과, 처리시간이 12초가 되었다면, 이 경우 오버헤드가 3초 단축되었다고 말한다.

5. 디자이너의 능력을 가정함
	 - 템플릿 시스템은 드림위버와 같은 위지윅 편집기에서 템플릿이 보기 좋게 표시되도록 설계해서는 안 된다. 위지윅 편집기는 너무 제한적이며 해당 구문이 깔끔하게 표시되지 않도록 한다. 장고는 템플릿 장성자가 HTMl을 직접 편집하는 것이 편리할 것이라고 가정한다.

6. 공백을 명확하게 처리함
	- 템플릿 시스템은 공백으로 마술적인 일을 해서는 안 된다. 템플릿에 공백이 포함돼 있으면 시스템은 공백을 테스트를 처리하는 것처럼 처리해야 한다. 템플릿 태그에 없는 공백은 모두 표시돼야 한다.

7. 프로그래밍 언어를 발명하지 않음
	- 템플릿 시스템은 의도적으로 다음을 허용하지 않는다
		- 변수에의 할당
		- 고급 로직
	- 목표는 프로그래밍 언어를 발명하는 것이 아니라 프레젠테이션 관련 결정을 내리는 데 필수적인 분기 및 루핑과 같은 프로그래밍에 민감한 기능을 제공하는 것이다. 장고 템플릿 시스템은 템플릿을 프로그래머가 아니라 디자이너가 가장 자주 작성하는 것을 인식해야 하므로 파이썬을 잘 알고 있다는 가정을 해서는 안된다.

8. 안전과 보안을 보장함
	- 템플릿 시스템은 기본적으로 데이터베이스 레코드를 삭제하는 명령과 같은 악의적인 코드의 포함을 금지해야 한다. 이것은 템플릿 시스템이 임의의 파이썬 코드를 허용하지 않는 또 다른 이유다.

9. 확장을 할 수 있음 
	- 템플릿 시스템은 고급 템플릿 작성자가 기술을 확장할 수 있다는 것을 알고 있어야 한다. 이것은 사용자 정의 템플릿 태그 및 필터의 철학이다.

	
## template {% extends %}

- 템플릿을 로드하면 템플릿 엔진은 {% extends %} 태그를 보고, 이 템플릿이 자식 템플릿이라는 것을 알게된다. 이 엔진은 즉시 부모 템플릿을 로드한다.
- 이 시점에서 템플릿 엔진은 base.html에 있는 3개의 {% block %} 태그를 확인하고 해당 블록을 자식 템플릿의 내용으로 바꾼다. 따라서 {% block title %} 에서 정의한 제목 {% block content %}와 같이 사용된다.
- 자식 템플릿은 바닥글 블록({% block footer %}) 정의하지 않으므로 템플릿 시스템에서는 부모 템플릿의 값을 대신 사용한다. 상위 {% block %} 태그 내 콘텐츠는 항상 예비로 사용된다.

- 상속을 사용하는 일반적인 방법 중 하나는 다음 3수준의 접근이다
	 1. 웹 사이트의 주요 모양과 느낌을 갖도록 하는 base.html 템플릿을 만든다. 이것은 거의 변하지 않는 내용이다.
	 2. 웹 사이트의 각 섹션에 base_SECTION.html 템플릿을 만든다(예: base_photos.html 및 base_forum.html). 이 템플릿은 base.html 확자하고 섹션 관련 styles/design을 포함한다.
	 3. 포럼 웹 페이지 또는 사진 갤러리와 같은 각 유형의 웹 페이지에 대한 개별 템플릿을 만든다. 이 템플릿은 해당 섹션 템플릿을 확장한다.


- 상속을 사용하기 위한 몇가지 지침
	1. 템플릿에서 {% extends %}를 사용하는 경우, 해당 템플릿에서 첫 번쨰 템플릿 태그여야 한다. 그렇지 않으면 템플릿 상속이 작동하지 않는다.
	2. 일반적으로 기본 템플릿에 {% block %} 태그가 많을수록 좋다. 자식 템플릿은 모든 부모 블록을 정의할 필요가 없으므로 여러 블록에서 적잘한 기본값을 채운 후 자식 템플릿에 필요한 템플릿만 정의한다. 적은 수의 후크보다 더 많은 후크를 갖는 것이 좋다.
	3. 여러 템플릿에서 코드를 복사하는 경우에는 해당 코드를 부모 템플릿의 {% block %}으로 이동해야 한다.
	4. 상위 템플릿에서 블록의 콘텐츠를 가져와야 하는 경우에는 {{block.super}}를 사용한다. 이 변수는 상위 템플릿의 랸더링된 텍스트를 제공하는 "마법"변수다. 이 변수는 부모 블록의 내용을 완전히 오버라이드하는 대신 추가하려는 경우에 유용하다.
	5. 동일한 템플릿에 같은 이름의 여러 {% block %} 태그를 정의할 수는 없다. 블록 태그가 "양쪽" 방향으로 작동하기 때문에 이러한 제한이 있게 된다. 즉, 블록태그는 채울 구멍만을 제공하는 것이 아니라 부모의 구멍을 채우는 내용도 정의 한다. 템플릿에 유사하게 이름이 지정된 2개의 {% block %} 태그가 있다면 해당 템플릿의 부모는 사용할 블록 콘텐츠가 어느 것인지 알 수 없다.
	6. 여러분이 {% extends %} 에 전달한 템플릿 이름은 get_template()이 사용하는 것과 같은 방법을 사용해 로드된다. 즉, 템플릿 이름이 DIRS 설정 또는 현재 장고 앱의 "templates" 폴더에 추가된다.
	7. 부분의 경우 {% extends %}에 대한 인수는 뭄ㄴ자열이지만, 런타인까지 상위 템플릿 이름을 모르는 경우에는 변수가 될 수 있다. 