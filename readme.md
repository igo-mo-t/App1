1) Модель данных разработана таким образом, что есть дилеры компании Skoda в разных городах, а также есть автомобили марки Skoda. Один дилер может продавать несколько разных моделей Skoda, и также у одной модели машины может быть несколько разных дилеров. Установлена связь многие ко многим.

2) Для запуска приложения необходима установка пакетов из файла requirements.txt

3) endpoints:

http://127.0.0.1:5000/cars (methods: GET, POST)
http://127.0.0.1:5000/dealers (methods: GET, POST)      
http://127.0.0.1:5000/dealer/<string:name> (methods: GET, PUT, DELETE)
http://127.0.0.1:5000/car/<string:model> (methods: GET, PUT, DELETE)

4) Примеры запросов:

В начале желательно создать автодилеров.
Во всех запросах вложенные данные (ключи) в запрос эквивалентны названию полей (колонок) в модели данных ресурса.
Исключение - создание новой модели машины (methods: PUT, POST), в запрос нужно также вкладывать 'city' который равен одному из существующих городов в модели данных дилеров. Это сделано, чтобы сразу образовывалась связь с дилерами у которых будет продаваться машина.

<!-- -POST http://127.0.0.1:5000/cars/ (добавление несуществующей машины) -->
request
{
    "equipment": "TIPO_MEGA",
    "model": "VITYA_KATYA_SUPERCAR",
    "price": 10090909090920,
    "city": "SPB"
}

response
{
    "New car": {
        "equipment": "TIPO_MEGA",
        "model": "VITYA_KATYA_SUPERCAR",
        "price": 10090909090920
    },
    "Dealers": [
        {
            "name": "Griffin-auto",
            "city": "SPB"
        },
        {
            "name": "Sigma",
            "city": "SPB"
        }
    ]
}

<!-- -PUT http://127.0.0.1:5000/car/SKODA_RS (добавление несуществующей машины) -->
 
 request
 {
    "equipment": "nishii",
    "model": "SKODA_RS",
    "price": 900,
    "city": "SPB"
}

response
{
    "New Car": {
        "equipment": "nishii",
        "model": "SKODA_RS",
        "price": 900
    },
    "Dealers": [
        {
            "name": "Griffin-auto",
            "city": "SPB"
        },
        {
            "name": "Sigma",
            "city": "SPB"
        }
    ]
}

<!-- -PUT http://127.0.0.1:5000/car/"SkodaOctavia (обновление данных по машине) -->

request
{
    "equipment": "nishii",
    "model": "SkodaOctavia",
    "price": 100920,
    "city": "VSEV"
}

response
{
    "Update Car": {
        "equipment": "nishii",
        "model": "SkodaOctavia",
        "price": 100920
    }
}