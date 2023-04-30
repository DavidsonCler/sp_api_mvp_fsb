# API - Space Pedidos - Davidson Cler do Nascimento

Este pequeno projeto foi baseado com o exemplo dado na disciplina de  **Desenvolvimento Full Stack Básico** 

O intuito desse desenvolvimento foi, além do aprendizado, explorar nuances do App base, e implementar funções novas, com uma nova cara e bem mais interativo.
Existem mais coisas para se fazer nesse projeto, como qualquer outro programa, mas está funcional em tudo que oferece.


#### Espero que curtam!!!
---
## Como executar ===== Nada de diferente...


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas. Foi utilizado jquery além destes, mas ele está na base da pagina html, sem necessidade de baixar-lo.

## Como de Praxe, vamos usar o env, para não misturarmos os pacotes de nossos projetos!
> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
