# machine_learning_business_project_python_docker_flask
Итоговый проект курса "Машинное обучение в бизнесе"

Стек:

- ML: sklearn, pandas, numpy
- API: flask
- Данные: с kaggle - https://www.kaggle.com/datasets/adityakadiwal/water-potability

Задача: предсказать по указанным характеристикам, пригодна вода для питья или нет. Бинарная классификация

Используемые признаки:

- ph (numerical, float)
- Hardness (numerical, float)
- Solids (numerical, float)
- Chloramines (numerical, float)
- Sulfate (numerical, float)

Преобразования признаков: StandardScaler

Обработка пропусков: SimpleImputer (mean)

Модель: RandomForestClassifier

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/demiorca/mlb_project_python_docker_flask.git
$ cd mlb_project_python_docker_flask
$ docker build -t demiorca/mlb_project_python_docker_flask .
```

### Запускаем контейнер и проверяем работоспособность

Здесь вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу), то есть путь к файлу rf_pipeline.dill:
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/models demiorca/mlb_project_python_docker_flask
```

После этого Docker автоматически запустит оба файла: run_server.py и run_front_server.py

Проверить работоспособность можно следующими командами:
```
$ docker ps -a
$ docker logs <вставьте id созданного контейнера>
```

В строчке "Running on..." будет указан адрес, который можно открыть в браузере. С портом 8181 веб-версия с фронтендом (формой для ввода значений). 

### Запускаем скрипт run_server.py

Если в Docker всё запустилось корректно, то проверку скрипта можно осуществить без запуска скрипта run_server.py в среде разработки Python.

Либо же скрипт можно запустить в любой среде разработки Python (например, PyCharm). Нужен файл run_server.py из папки app.

### Проверяем работоспособность в Jupyter Notebook (или в другой среде разработки, которая поддерживает ipynb-формат, например, JupyterLab или DataSpell)

Откройте файл project_step3.ipynb и запустите код. Под блоком "Примеры" можно вводить любые данные (5 признаков) в функции get_prediction(()) и проверять

### Запускаем скрипт run_front_server.py

Если в Docker всё запустилось корректно, то проверку скрипта можно осуществить без запуска скрипта run_front_server.py в среде разработки Python.

Либо же скрипт можно запустить в любой среде разработки Python (например, PyCharm). Нужен файл run_front_server.py из папки app/front. Скрипт run_server.py должен быть предварительно запущен. Скрипт run_front_server.py позволяет вводить значения в браузере и выводить результат в подготовленных страницах.

### Проверяем работоспособность в веб-форме на localhost:8181

Откройте в браузере страницу http://localhost:8181 (либо http://127.0.0.1:8181, но адрес может зависеть от системы). Проверить адрес можно в логе запущенного скрипта (в docker logs или в среде разработки Python).

Нажмите на кнопку "Entering data". В соответствующих полях введите значения признаков, после чего нажмите на кнопку "Predict". После этого откроется страница с результатом вероятности того, пригодна ли вода для питья.
