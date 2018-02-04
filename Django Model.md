# Django Model

## ORM의 사용이유

1. 인트로스펙션은 오버 헤드를 필요로 하여 불완전하다. 장고는 편리한 데이터-접근 API를 제공하기 위해 데이터베이스 레이아웃을 어떻게 해서든 알 필요가 있고, 이를 달성하기 위한 두 가지 방법이 있다. 첫째, 파이썬의 데이터를 명시적으로 설명하는 것이다. 둘떄, 데이터 모델을 결정하기 위해 실행 시 데이터베이스를 살펴보는 것이다
2. 이 두 번쨰 방법은 테이블에 대한 메타 데이터가 한곳에만 있기 때문에 상대적으로 명확해 보이지만, 몇 가지 문제가 발생한다, 첫째, 런타임 시 데이터베이스를 살펴볼 때는 분명히 오버 헤드가 필요하다. 해당 프레임워크가 요청을 처리할 때마다 데이터베이스를 살펴보거나 심지어 웹 서버가 초기화된 경우에도, 허용할 수 없는 수준의 오버헤드가 발생한다. 둘째, 일부 데이터베이스, 특히 이전 버전의 MySQL은 정확하고 완전한 검사를 위한 충분한 메타 데이터를 저장하지 않는다.
3. 파이썬은 작성하는 것은 재미있고, 파이썬에서 모든 것을 유지하게 되면 여루분으니 두뇌가 "상황 전환"을 해야 하는 횟수를 제한하게 만든다. 여러분 스스로 가능한 한 오랫동안 단일 프로그래밍 환경/사고방식을 유지하면 생산성 향상에 도움이 된다. SQL을 작성한 후 파이썬을 작성하고 다시 SQL을 작성하면 방해를 받게 된다.
4. 데이터 모델을 데이터베이스가 아닌 코드로 저장하면 버전 제어하에 모델을 좀 더 쉽게 유지할 수 있다. 이렇게 하면 데이터 레이아웃의 변경 사항을 쉽게 추적 할 수 있다.
5. SQL은 데이터 레이아웃에 관한 일정 수준의 메타 데이터만 허용한다. 예를 들어, 대부분의 데이터베이스 시스템은 장고 모델과 달리 전자 메일 주소나 URL을 나타내는 특수한 데이터 유형을 제공하지 않는다. 상위 수준 데이터 유형의 장점은 높은 생산성과 재사용할 수 있는 코드다.
6. SQL은 데이터베이스 플랫폼 간에 일관성이 없다. 예를 들어, 웹 응용 프로그램을 배포하는 경우 MySQL, PostgreSQL 및 SQlite용 CREATE TABEL문을 별도로 설장하는 것보다 데이터 레이아웃을 설명하는 파이썬 모듈을 배포하는 것 이 훨씬 실용적이다.

## update()

- Apress Publisher를 업데이트 한다고 가정해보자. save()를 사용하면 다음과 같을 것이다.

```
 p = Publisher.objects.get(name='Apress')
 p.name = 'Apress Publishing'
 p.save()
```

- 이것은 대략 다음 SQL로 변환된다.

```
SELECT id, name, adress, city, state_province, country, website
FROM books_publisher
WHERE name = 'Apress';

UPDATE books_publisher SET
	name = 'Apress Publishing',
	address = '2855 Telegraph Ave.',
	city = 'Berkeley',
	state_province = 'CA',
	country = 'U.S.A.',
	website = 'http://www.apress.com/'

WHERE id = 52;
```

-  이 예제에서 장고의 save() 메서드는 name 열뿐만. 아니라 모든 열값을 설정한다는 것을 알 수 있다. 일부의 다른 프로세스로 인해 데이터베이스의 다른 열이 바뀔 수 있는 환경에 있다면 변경해야 하는 열만 변경하는 것이 어 더 좋다. 이렇게 하려면 QuerySet 객체에서 update() 메서드를 사용해야 한다.

```
Publisher.objects.filter(id=52).update(name='Apress Publishing')
```

- SQL 변환은 훨씬 효율적이여, 경쟁 조건은 없다.

```
UPDATE books_publihser
SET name = 'Apress Publishing'
WHERE id = 52'
```