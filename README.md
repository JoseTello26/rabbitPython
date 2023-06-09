# rabbitPython
## Python Container
Execute (replace env variables): 
```
docker run -d --rm  -e RABBITMQ_HOST='172.0.0.1' -e RABBITMQ_PORT='5672' -e POSTGRES_USER='postgres' -e POSTGRES_PASSWORD='postgres' -e POSTGRES_HOST='172.0.0.2' -e POSTGRES_PORT='5432' josetello26/rabbit-python:1.0
```
## Postgres Container
```
docker run -d --rm josetello26/rabbit-postgres:1.0
```
