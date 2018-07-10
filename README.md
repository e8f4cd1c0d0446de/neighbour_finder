# neighbour_finder

Инструмент neighbour_finder «Поиск соседей» предназначен выступать в роли сервера выполняющего поиск соседей поблизости

# Требования

Для работы «Поиска соседей» требуется:

## Наличие операционной системы
Ubuntu LTS будет достаточно

## Наличие интерпретатора
```
sudo apt-get install -y python3
```

## Наличие сервера базы
```
sudo apt-get install -y mongodb-org
sudo service mongod start
```

## Наличие зависимостей
```
pip3 install tornado motor
```

## Подготовленная база данных
```
mongo --host 127.0.0.1:27017
use neighbour_finder
db.neighbours.createIndex( { location : "2dsphere" } )
```

# Пример использования
```
# установить клиент
sudo apt-get install -y httpie
# добавить соседа
http POST 127.0.0.1:8888/neighbours x=10.1 y=20.3 name='paul'
# получить список соседей выстроеннных по удаленности
http '127.0.0.1:8888/neighbours?x=1&y=1&limit=7'
```
