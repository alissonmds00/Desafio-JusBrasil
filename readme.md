Requisitos para a aplicação:
- Navegador Chrome
- Python v3.12.5

<h1>Explicação do funcionamento</h1>
A aplicação possui um crawler que faz requisições para um site o qual está configurado. Na aplicação em questão, a configuração foi feita para que ele execute o crawling no site do TJCE e TJAL. Através do número de processo ele identifica e faz as devidas adaptações para que o número de processo só seja consultado no seu devido TJ.
As configurações das requisições ocorrem em alguns arquivos como: os arquivos do diretório service: app.py (que reúne as regras de execução do crawler), e consulta_service que é responsável pelas regras de armazenamento no banco de dados.
Ademais, no diretório utils possui as ferramentas que cuidam das funcionalidades e tratamentos de dado da aplicação, e também podem ser re-configurados caso necessário.

<h1>Como executar</h1>:
0- É importante a criação de um arquivo nomeado como ".env", em que os valores devem ser copiados e colados do arquivo ".env,example", embora funcione sem.

1- Criação do virtual environment:
  python -m venv [venv]

2- Ativação do venv:
  venv/Scripts/activate

3- Instalação das dependências:
  pip install -r requirements.txt

4- Executar as migrates no db (padrão: sqlite):
  python manage.py migrate

5- Executar a API:
  python manage.py runserver
  
URL padrão: http://127.0.0.1:8000/

6- Para fazer a requisição da consulta:
  fazer uma requisição do método get para a URI: http://127.0.0.1:8000/processos/numeroDoProcessoSemPontosEHífens


<h1>Limitações</h2>
Devido à não padronização do nome dos atributos entre os sites, no primeiro e segundo grau, o crawler precisa buscar por nomes alternativos, o que aumenta consideravelmente o tempo de execução, de forma a não comprometer a coleta de dados que não são carregados instantaneamente.

<h1>Considerações finais</h1>
Preferi não armazenar separadamente as informações de movimentações e partes, por acreditar que o tratamento de dados a partir da requisição iria performar de uma maneira melhor através do front-end. Portanto, são retornadas em forma de array.


