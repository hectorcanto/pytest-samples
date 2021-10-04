
### Testing efectivo con Pytest

[@hectorcanto_dev](https://twitter.com/hectorcanto_dev)

[slideshare.net/HectorCanto](https://www.slideshare.net/HectorCanto/)

[github.com/hectorcanto/pytest-samples](https://github.com/hectorcanto/pytest-samples)

[PyConEs 2021](https://2021.es.pycon.org/)

It will published in slideshare and Github

## Objetivo

Nos centraremos en *testing unitario con Pytest*, pero
muchas cosas también sirven para otros frameworks y lenguajes

Esta será una charla principalmente practica
pero hablaremos un poco de por qué es importante para meternos en materia

## Por qué pytest

Es un framework maduro y muy potente

Muy bien documentado y compatible con muchas herramientas

### Por qué efectividad en testing

El Testing ocupa buena parte de nuestro tiempo programando

- Mejor testing, mejor Software
- Cuanto más efectivos, más tiempo para otras cosas

probabl. 50% del tiempo
Si reducimos ese tiempo a la mitad, ahorraremos el 25% de nuestro tiempo trabajando

### Testear es importante

- Garantiza que todo el código funciona cuando desarrollamos mejoras
- Documenta con ejemplos y da contexto
- Es un entorno muy útil para depuración
- **Habilita la refactorización**

Artículo: [Tips and tricks for unit tests](https://medium.com/worldsensing-techblog/tips-and-tricks-for-unit-tests-b35af5ba79b1)

More about this in this article I wrote a couple of year ago

#### Efectividad significa

- Tests rápidos y manejables
- Desarrollo fácil y código mantenible
- Accesible y leíble para todo el mundo

Que se facil ampliar los casos, crear nuevos tests
Para nuestros compañeros y para nuestro yo futuro

#### Como conseguimos esta efectividad

- Utilizando pytest en toda su potencia
- Entendiendo la teoría: mocks, fixtures, parametrización
- Aprovechamiento de librerías y plugins
- Buenas prácticas generales de código
- Estrategias y Sentido común

Ahora veremos ejemplos reales

## Fases de un test

Los test se dividen en 3 fases conocidas como la triple AAA

- Arrange: Preparación
- Act: Ejecución
- Assert: Validación

Propondremos ideas para las tres

Pasamos a la parte práctica
Todos los ejemplos son ejecutables y están disponibles en Github
...
Pero antes empezaremos por cómo lanzamos nuestra suite

## Lanzar la Suite de tests

- Opciones de pytest
- Marcadores
- Selección de test

*Solo lanzaremos lo que necesitemos*

#### Opciones de pytest

```bash
pytest --help
pytest tests/folder/test_file.py::test_name
pytest -m smoke
pytest -k users
```
Podemos filtrara de muchas maneras

El primer comando que quiero que recordéis es el help

#### Suite: repetir test fallidos

```bash
pytest --fail-first
pytest --last-failed
pytest --failed-first
````
Daremos prioridad a los tests fallidos

    Plugin: pytest-xdist

Estas son algunas opciones útiles para reducir el número de tests ejecutados
OS añado pytest-xdist que permite ejecutar test en paralelo
Es un plugin complicado, que os puede dar problemas, pero merece la pena intentarlo
La reducción de tiempo es muy grande y lo agradecermos en suites muy grande

#### Suite: tests específicos

```python
def test_users_creation():
    ...

def test_users_update():
    ...
```

```bash
pytest -k users
```
El _naming_ es importante

Esto nos permite seleccionar tests por una parte de su nombre
Clean Code

#### Suite: marcadores

```python
@pytest.mark.slow
@pytest.mark.current
@pytest.mark.skip(reason="whatever")
@pytest.mark.xfail
def test_this():
    ...
```

```bash 
pytest -m current -s  -v
pytest -m "slow and not integration"
pytest -m "smoke and unit" 
```

Ejemplos: smoke, unit, integration, current, slow

Tests marcados con current, con captura de terminal y verbosidad

#### Suite: marcadores globales

```python
# Per module
pytestmark = pytest.mark.auth
pytestmark = [pytest.mark.deletion, pytest.mark.api]

# Per class
class TestClass:
    pytestmark = pytest.mark.special
```
Es fácil marcar grupos de tests

Esto nos permite seleccionar tests por una parte de su nombre

#### Suite: Estructura

```bash
tree tests/ --dirsfirst

tests/
├── smoke/
└── unit/
│   ├── service/
│   └── persistance/
├── integration/
│
├── fixtures/
├── factories/
├── conftest.py
├── aux.py
└── __init__.py
```

Ahora nos vamos a meter un poco con la estructura del directorio de tests
Es bueno tener una estructura recurrente y esta nos sirve para los marcadores
Fijaros en smoke, unit, integration, persistance ..

#### Suite: marcadores automáticos

```python
def pytest_collection_modifyitems(items):
    for item in items:
        if "/smoke/" in str(item.module):
            item.add_marker("smoke")
```

Coloca esto en `tests/conftest.py`

Asi marcaremos todos los tests de un subdirectorio X com un marcador dado

#### Recomendación: smoke tests

- Comprobar config y entorno
- Instanciación con valores por defecto
- Errores y casos simples 

Los lanzaremos los primeros, local y CI

Evitaremos sustos y ahorraremos tiempo

#### Suite: ordenación

```python
@pytest.mark.first
@pytest.mark.second
@pytest.mark.last
```

El order es importante para `smoke` y CI

Dejaremos los lentos para el final

    Plugins: pytest-ordering, pytest-randomly

De todas formas, es bueno ejecutar los tests en orden aleatoria y cambiante
para evitar efectos colaterales entre tests

### Suite: entorno

```ini
# setup.cfg
[tool:pytest]
env =
    PYTHONBREAKPOINT=ipdb.set_trace
    APP_ENVIRONMENT=test
    CACHE=memory
    DEBUG=1
    VAR=value
```
Separamos entornos local y de test

    Plugin: pytest-env

Esto nos permite separar el entorno local del de la suite de test completamente

### Suite: entorno II

```python
def test_with_different_env_vars(monkeypatch):
    monkeypatch.setenv("CACHE", "nocache")
    monkeypatch.delenv("VAR")
```

    Fixture: monkeypatch

Si queremos cambiar el entorno puntualmente
monkeypatch es un fixture muy util que veremos de nuevo mas adelante

## Setup

- Parametrization
- Fixtures
- Factories

También _Arrange_ o Preparación

#### Parametrización

```python
@pytest.mark.parametrize("entry, expected", (
    (1, True),
    (2, False),
    (None, False),
    ("hello", False),
)
def test_something(entry, expected: bool):
    result = function_under_test(entry)
    assert result == expected
```
En vez de hacer un test para cada caso

Reutilizaremos un test para todas las entradas

### Fixtures

Fixtures es el conjunto de elementos que establecemos para
crear un entorno concreto.

- los datos que preparamos
- El sistema en un estado concreto
- Elementos activos con el comportamiento "trucado"

#### Pytest fixtures

```python
@pytest.fixture
def example_fixture()
    now = datetime.utcnow()
    do_setup(now)
    yield now
    do_teardown()  # clean up
```
Fixtures con setup, teardown o ambos

Podemos devolver una estructura de datos,
un elemento modificado
un objeto trucado
...
Y en el teardown limpiamos, recuperamos todoa el estado normal
quitamos datos de ficheros y bases de datos

#### Ejemplo de fixture

```python
@pytest.fixture
def load_data(db_client):
    my_user = User(name="Hector", last_name="Canto")
    db_client.add(my_user)
    yield my_user  # usable as parameter
    db_client.delete(my_user) 
```

Aquí vemos otro ejemplo típic.
Fijáos que esta fixture tiene un parámetro 'db_client' que es otra fixture
Como podéis ver se pueden enlazar fixtures
Pero ojo, algunas fixtures pueden no ser compatibles con otras, pero el framework os lo chiva

#### Usar una fixture

```python
@pytest.mark.usefixtures("load_data")
def test_with_fixtures(example_fixture):
     result, error = system_under_test(example_fixture)
     assert result
     assert not error
```

Colocad vuestras fixtures en cualquier `conftest.py`

para no tener que importarlas

Se cargan automáticamente cuando se necesitan
Tenéis un ejemplo de una fixture que utilizamos como parámetro, y otra que no.

#### Reutilizar fixtures 

```python
@pytest.fixture(scope="session")
def test_settings():
     yield get_settings(test=True)
```

Scopes: sesión, módulo, clase o función

Hay fixtures que sabemos que con ejecutarlas una vez es suficiente
Usando scope podemos limitar la acción de una fixture a una clase, modulo o toda la sesion
Esto es muy típico para crear y destruír tablas, limpiar caché, borrar archivos

#### Fixtures automáticas

```python
@pytest.fixture(autouse=True)
def clean_db(db_client):
    yield db_client
    for table in db_client.tables:
        db_client.truncate()     
```
Se autoejecuta sola

Se apoya en otra fixture anterior

### Fixtures de datos

    Recomendación: crear datos para fixtures *programáticamente*

- Constantes que importamos
- Funciones para generar
- Factorías

- Evitar JSON crudos, archivos de texto ...

Desde Python
en las funciones, nos centramos en la diferencia, qué es lo relevante para el tests
en los datos hay mucha informacion repetida, que crea ruído
En esta parte me voy a centra en las factorías, que es la manera más eficiente de crear datos

#### Setup: Factory

```python
from factory import StubFactory

class ObjectFactory(StubFactory):
    name: str = "value"
    
my_ojb = ObjectFactory()
assert my_obj.name == "value"

other = ObjectFactory(name="another value")
assert other.name == "another value"
```

    Librería & plugin: factoryboy, pytest-factoryboy

Y en concreto me centraré en las librerías Factory y Faker
StubFactory es el caso más simple de factoría, con la que creamos un objeto
Podemos designar valores por defecto, o designar cuando instanciamos

#### Factory & Faker

```python
from factoryboy import Faker, SelfAttribute
from factory.fuzzy import FuzzyInteger

class ObjectFactory(StubFactory):
    name: str = Faker("first_name_male")
    last_name: str = Faker("last_name")
    full_name: str = SelfAttribute(lambda self: f"{self.name} {self.last_name}")
    phone: str = Faker("phone_number", local="en_GB")
    money: int = FuzzyInteger(1, 1000)
```
Genera valores a discreción

    Librería: Faker

Y el complemente perfecto de factoryboy es faker
Una librería para generar valores aleatorios o en determinados rangos
Podemos usarlas en tiempo de ejecución o para generar algo y guardarlos permanentemente

#### Model Factory

```python
from factory import alchemy, RelatedFactory

class UserFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = Session

    id = LazyFunction(lambda: randint(1, 1_000_000))
    location = RelatedFactory(LocationFactory)
    created_at = Faker(
        "unix_time", 
        start_datetime=datetime(2015, 1, 1), 
        end_datetime=datetime(2019, 12, 31)
    )
```
Se puede usar con Django, SQLAlchemy y Pymongo

El siguiente caso, más complejo, son las factorías de Modelos
Estas, nos permiten escribir en base de datos, o generar objectos pre-escritura
Esto es super potente por que en vez de mantener fixtures en SQL, que es muy costoso
lo hacemos en Python, directamente basándonos en nuestros modelos
Prestad especial atención a la RelatedFactoyr, esto nos permite crear modelos a través
de relaciones, y lo resuelve el propio ORM

#### Batches & Dict Factory

```python
factory.build(dict, FACTORY_CLASS=UserFactory)
UserFactory.create_batch(5)

class UserDictFactory(DictFactory)
  ...
```
Genera _inputs_ para tu API o función 

No sólo eso, si no que podemos generar múltiples instancias en masa (batch)
o generar diccionarios equivalentes que podemos utilizar para atacar nuestra API
La diferencian entre build y create es que una escribe en DB y la otra no
Y hasta aquí, el mundo de las factories da para mucho más

### Ejecución o Act

- Controlar el tiempo
- Test doubles: mocks y familia

#### Freezegun

```python
from datetime import datetime
from freezegun import freeze_time

@freeze_time("2012-01-14")
def test_2012():
    assert datetime.now() == datetime(2012, 1, 14)

    with freeze_time("2018-01-01"):
        assert datetime.now() > datetime(2012, 1, 4)
```
Para el tiempo a tu antojo

    Library: freezegun

#### Freezer

```python
from datetime import datetime

def test_freezer_move(freezer):
    now = datetime.now()
    freezer.move_to('2017-05-20')
    later = datetime.now()
    assert now != later

@pytest.mark.freeze_time('2017-05-21')
def test_freeze_decorator():
    assert datetime.now() == datetime(2017, 5, 21)
```

    Fixture: freezer

#### Otras librerías temporales

timeago -  moment - pytime - arrow

```python
timeago.format(timedelta(seconds = 60 * 3.4))  # 3 minutes ago
moment.date(2012, 12, 19).add(hours=1, minutes=2, seconds=3)  # no more deltas
pytime.next_month('2015-10-1')  # again, no-more-deltas
arrow.utcnow().span('hour')  # 2 datetimes in one line
```

### Ejecución: test doubles

Los Test doubles substituyen a algún elemento activo con el comportamiento deseado

#### Tipos de test doubles

- Dummy: objeto que se pasa pero no se usa
- Fake: Implementación simplificada que funciona
  - fake server, in-memory cache
- Stubs: Respuestas prefabricadas, reemplazo total
- Mocks: Reemplazo parcial, respeta interfaces
- Spies: No intercepta, solo registra

`martinfowler.com/bliki/TestDouble.html`

### Mock library

La mayoría de nuestros dobles se implementan con mock

    Library: mock - Plugin: pytest-mock  - Fixture: mocker

Vamos a ver algunos ejemplos reales

#### Python mocks

```python
def test_mock_patching(mocker):
    url = "https://2021.es.pycon.org/" 
    mocked = mocker.patch.object(requests, "get", return_value="intercepted")
    mocker.patch.object(requests, "post", side_effect=ForbiddenError)
    response = requests.get(url)
    assert response == "intercepted"
    assert mocked.called_once()
```

Normalmente parcheamos métodos y funciones
aunque también atributos

#### Stubs

```python
def test_stubbing(monkeypatch):

    def mock_exist(value):
        print(f"{value} exists")
        return True

    monkeypatch.setattr(os.path, 'exists', mock_exist)
    assert os.path.exists("/believe/me/I/exist")
```

Para parchear os recomiendo hacerlo con monkeypatch, que viene incluido en pytest base
por debajo usa la librería mock. Tiene la ventaja de que desmonta el mock después de la ejecución
y la desventaja que solo se puede usar con 'scope' de función

#### Espía

```python
def test_with_spy(mocker):
    url = "https://2021.es.pycon.org/"
    spy = mocker.spy(requests, "get", wraps=requests.get)
    response = requests.get(url)
    assert response.status_code -= 200
    spy.assert_called_once(), spy.mock_calls
    spy.assert_called_with(url)
```
No intercepta, solo registra llamadas

Realmente, todos los mocks tienen un espía, pero los demás hacen intercepción

#### Interceptores

```python
def test_with_http_interceptor(requests_mock):
    # arranges
    url = "http://tests.com"
    requests_mock.get(url, json={"key": "value"})
    # action
    response = requests.get(url)
    
    assert "key" in response.json()
```

Intercepta llamadas y devuelve lo que quieras

    Library: requests_mock

Y de ejecución nos quedan los interceptores puros
Solo hablaremos de esta, pero hay muchos más, para otrós protocolos tambien

### Validación

```python
def test_one():
    expected = 5
    result = system_under_test()
    assert result
    assert result is not None
    assert result == expected
    assert result > 3
```
Validamos sentencias lógicas

#### Mensajes de error

```python
response = requests.get(url)
assert response.json() == expected, response.text()
```
En caso de `AssertionError`

exponemos info extra

#### Comparaciones

```python
import pytest, math

assert 2.2 == pytest.approx(2.3, 0.1)
assert math.isclose(2.2, 2.20001, rel_tol=0.01)
```
No perdáis el tiempo 

con errores de bulto y redondeos

#### Comparaciones: listas y sets

```python
my_list = [1, 1, 2, 3, 4]
other_list = [4, 3, 2, 1]

list_without_duplicates = list(set(my_list))
diff = set(my_list) ^ set(other_list)
assert not diff
```
No os volváis locos con valores repetidos 

ni bucles comparando listas

#### Comparaciones: dicts

```python
from deepdiff import DeepDiff

def test_dicts(parameter, expected):
    result = system_under_test(parameter)
    diff = DeepDiff(result, expected, exclude_paths=(f"root['updated_at']",), ignore_order=True)
    assert not diff, diff
```

No perdáis el tiempo ordenando dicts 

ni calculando y borrando elementos difíciles 

    Library: deepdiff

#### Comprobaciones pospuestas

```python
def test_delayed_response(requests_mock):
    url = "http://tests.com"
    requests_mock.get(url, json={"key": "value"})

    response = requests.get(url)

    expect(response.status_code == 200, response.status_code)
    expect(response.json() == {}, response.text)
    assert_expectations()
```

    Library: delayed-assert

Si por algún motivo queremos hacer todas las comprobaciones de una vez o al final
utilizaremos delayed assert, que además nos da un retorno más trabajado

#### Delayed assert prompt

```python
    def assert_expectations():
        'raise an assert if there are any failed expectations'
        if _failed_expectations:
>           assert False, _report_failures()
E           AssertionError: 
E           
E           assert_expectations() called at
E           "/home/hector/Code/personal/effective_testing/tests/unit/test_delayed_assert.py:12" in test_delayed_response()
E           
E           Failed Expectations : 1
E           
E           1: Failed at "/home/hector/Code/personal/effective_testing/tests/unit/test_delayed_assert.py:12", in test_delayed_response()
E           	ErrorMessage:	{"key": "value"}
E               expect(response.status_code == 200, response.status_code)

../../../.local/share/virtualenvs/effective_testing-QL_w0uj8/lib/python3.9/site-packages/delayed_assert/delayed_assert.py:74: AssertionError
```

### Validar logs

Los logs son ultra-importantes
- Monitorización y Métricas
- Flujo de programa y control de errores
- Especialmente importante en microservicios y serverless

Lo último que veremos en validación serán los log

    
#### Captura logs

```python
def test_log_capture(request, caplog):
    logger = logging.getLogger(request.node.name)
    caplog.set_level("INFO")
    dtt = "2021-10-02 10:55:00"
    msg = "captured message"
    expected_message = f"{dtt} INFO module:{request.node.name} {msg}"
    
    with freeze_time(dtt):
        logger.info(msg)

    with caplog.disabled():
         logger.info ("Any log here will not be captured")
         some_function_with_logs()
         breakpoint()
         
    with freeze_time(dtt):
        logger.info("captured message")
    
    result = caplog.records[0].msg
    assert result == expected_message
```

    Fixture: caplog, capsys, capfd

Aquí hay un extra muy interesante, que es la posibilidad de parar la captura
lo que es imprescindible para poder meternos con el debugger

### Bola extra: tests y debugger

- Los tests son pequeños entornos que controlamos
- Debug en máquinas reales es difícil o directamente imposible

```bash
pip install ipdb
PYTHONBREAKPOINT=ipdb.set_trace pytest -m current -s
```

    Usa los puntos de ruptura del IDE

### Ideas finales

- "Los tests son un pérdida de tiempo"
  - Realmente, nos ahorran mucho tiempo
- Tratar los tests como ciudadanos de primera:
- No hay proyecto pequeño para tener tests
- Pensad en vuestro yo del futuro
- Testead más que el "happy path"

### Recomendaciones

- Si algo os cuesta mucho...
  - seguro que hay una librería o receta que lo hace por vosotros
- Leed y releed la documentación
- Los frameworks son vuestros amigos

### Summary

_Fixtures_: monkeypatch, mocker, requests_mock, caplog, parametrize, mark

_Librerías_: factoryboy, faker, deepdict, freezegun, moment, ipdb

https://docs.pytest.org/

https://docs.pytest.org/en/latest/reference/plugin_list.html

### Se ha quedado fuera

Antipatrones, AWS, Docker, DBs, frameworks, asyncio

https://github.com/spulec/moto

https://github.com/localstack/localstack

http://blog.codepipes.com/testing/software-testing-antipatterns.html

https://www.yegor256.com/2018/12/11/unit-testing-anti-patterns.html

### Gracias

Espero que os gustara :)

Preguntas, sugerencias, errores ...?

https://github.com/hectorcanto/pytest-samples

https://www.slideshare.net/HectorCanto