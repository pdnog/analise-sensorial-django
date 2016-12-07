Para utilizar, precisa fazer o download de bootstrapform == 3.2.1 e reportlabs == 3.3.0

Para a instalação do reportlabs, instale o python3-dev na sua máquina (Linux baseado em debian: sudo apt-get install python3-dev)
Após a instalação do python3-dev, digite o comando: "pip install reportlabs==3.3.0" e pronto, não precisa nem colocar "reportlab" no settings.py

Vai ser necessário instalar para gerar os gráficos:
python-numpy
python-numpy-ext
python-matplotlib
python-imaging
python-numeric

Mudanças para o POSTGRESQL

1. sudo apt-get install postegresql python-psycopg2 libpq-dev
2. sudo su - postgres
3. psql
4. CREATE USER user_geral WITH PASSWORD 'senha123';
5. CREATE DATABASE server;
6. Acesse seu virtualenv
7. pip install psycopg2

Está pronto para usar.
