# Leaker

#### Описание
Проект для агрегирования, хранения и поиска данных. 

### Установка
```
docker build -t leaker:v0.1 .
```
#### Альтернативный вариант
```
pip install -r requirements.txt
```

### Использование
1. Создаем файл с конфигом .env и указываем данные, пример:
    ```
    MYSQL_USER=user
    MYSQL_PASS=pass
    MYSQL_HOST=192.168.1.1
    MYSQL_DB=leaker
    TABLE_PERFORMANCE_SIZE=1000
    DEBUG = True
    ```
2. Создаем в базу данных и пользователя в MySQL
   ```
   CREATE DATABASE leaker;
   CREATE USER 'leakeruser'@'%' IDENTIFIED BY 'Password';
   GRANT ALL PRIVILEGES ON leaker.* TO 'leakeruser'@'%';
   FLUSH PRIVILEGES;
   ```
3. Запускаем проект
   1. docker run -it -p5000:5000 leaker:v0.1
   или
   2. python app.py
4. Как загрузить данные
   1. Запускаем скрипт
    ```
       python3 loader.py data.csv
    ```  
   2. Определяем данные
      1. Указываем имя и url источника
      2. Указывает разделитель 
      3. Указываем колонки (можно объединять: 1 3 5+6+7)
