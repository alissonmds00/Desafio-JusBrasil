#Rodar a aplicação: 
-> python manage.py runserver 

#Criar um app novo
-> django-admin startapp [nome]

#Criar ambiente virtual
-> python -m venv [venv]

#Utilizar o venv
-> Powershell: .venv\Scripts\activate
-> CMD: venv/Scripts/activate.bat

#Instalando as bibliotecas
-> pip install -r requirements.txt

#Atualizando os arquivos do requirements.txt
-> pip freeze > requirements.txt

#Obtendo as atualizações do banco de dados
-> python manage.py migrate

#Executar os testes
-> python -m unittest desafio.tests.app_test