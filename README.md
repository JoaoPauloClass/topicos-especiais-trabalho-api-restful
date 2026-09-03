# Trabalho API Restful

Repositório destinado desenvolvimento de trabalho da matéria de Tópicos especiais de Software 
com o professor Rhafael Costa

## Como rodar o projeto

### Dependências

É necessária a instalação das dependencias por meio do comando:

```bash
pip install -r requirements.txt
```

### Banco de dados

Estamos utilizando o banco PostgreSQL para nosso projeto, é possível iniciá-lo com o comando docker abaixo:

```bash
docker run -d --name postgresql-server   -p 5435:5432   -e POSTGRESQL_PASSWORD=root -e POSTGRESQL_DATABASE=db_jogos  bitnami/postgresql:latest
```

### Migrations

Para realizar a migration e atualização das tabelas do banco, utilize os comandos na ordem abaixo:

```bash
flask db init
```

```bash
flask db migrate -m "Teste"
```

```bash
flask db upgrade
```

### Iniciar a aplicação

Para iniciar a aplicação utilize:

Windows
```bash
python run.py
```

Linux
```bash
python3 run.py
```

## Testes

Para testes, foi utilizado a ferramenta Bruno. Link para download: https://www.usebruno.com/downloads

### Importar requests

As requests utilizadas para testes estão disponíveis neste repositório na pasta `request-equipe-7`

Para fazer a importação, abra o Bruno e selecione:

![img.png](img.png)

Selecione a pasta `request-equipe-7` e a importação será realizada.