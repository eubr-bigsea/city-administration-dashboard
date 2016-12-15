Para executar a REST
--------------------

Versão completa:
----------------
Utilizaremos como referência um sistema utilizando o SO Linux, distribuição Ubuntu 14.04 LTS.

É necessário ter instalado os seguintes pacotes:
- python-dev
- libmysqlclient-dev
- python-virtualenv

A instalação desses pacotes é feita utilizando o comando: apt-get install <nome-do-pacote>

Feito isso, dentro da pasta da (tpanalytics/src/restful_api), crie um ambiente virtual utilizando o comando:

$ virtualenv .venv

Este comando irá criar um ambiente virtual na pasta '.venv'. Caso deseje utilizar outro nome para o ambiente
virtual, não commitar esta pasta.

Então, ativamos o ambiente virtual:

$ . .venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt

Feito isso, o ambiente está preparado para executar a REST. Agora crie uma cópia do arquivo 'config.ini.example'
com o nome 'config.ini'. O 'config.ini' deverá ser editado com as informações de credenciais do SGBD
entre outras. Há uma referência no final deste arquivo.


Versão preguiçosa:
------------------
Entre na pasta da REST e execute os comandos (sem o $):

$ sudo apt-get install python-dev libmysqlclient-dev python-virtualenv
$ virtualenv .venv
$ . .venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt

Configure o 'config.ini' conforme informações no final do arquivo.

----------
config.ini
----------

[Database]
host = put_host_here # host/ip do bd. Exemplos: 143.41.34.145 , enderecodobanco.com
port = put_port_here # porta em que o bd está sendo executado. Exemplo: 10333
user = put_user_here # nome do usuário do bd. Exemplo: cganalytics
passwd = put_password_here # senha do usuário do bd. Exemplo: senhadobanco
db_name = put_dbname_here # nome do esquema do banco. Exemplo: tpanalytics

[REST]
port = put_port_here # porta em que a REST ficará disponível
secret_key = put_secret_here # chave secreta para criptografar a sessão - essa chave não pode ser pública e só deve constar aqui

