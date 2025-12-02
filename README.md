# Expense Control API

API REST para gerenciamento de transações financeiras, desenvolvida como solução para o desafio de estágio backend da IUPI.

## Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Endpoints da API](#endpoints-da-api)
- [Exemplos de Uso](#exemplos-de-uso)
- [Testes](#testes)

---

## Visão Geral

Esta API foi desenvolvida para gerenciar transações financeiras pessoais, permitindo o controle de receitas (*income*) e despesas (*expense*). O sistema oferece:

- Operações CRUD completas para transações
- Filtros por descrição e tipo de transação
- Paginação de resultados
- Endpoint de resumo financeiro com agregação de dados
- Validações de entrada robustas

---

## Arquitetura

O projeto foi desenvolvido seguindo os princípios da **Clean Architecture**, garantindo separação de responsabilidades, testabilidade e manutenibilidade do código.

### Diagrama da Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    API REST (Django REST Framework)           │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │  │
│  │  │    Views    │  │  Serializers │  │        URLs         │   │  │
│  │  └──────┬──────┘  └──────────────┘  └─────────────────────┘   │  │
│  └─────────┼─────────────────────────────────────────────────────┘  │
└────────────┼────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                            │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                         Use Cases                             │  │
│  │  ┌────────────────┐  ┌─────────────────┐  ┌───────────────┐   │  │
│  │  │ CreateTransaction │ │ ListTransactions │ │  GetSummary   │   │  │
│  │  └────────────────┘  └─────────────────┘  └───────────────┘   │  │
│  │  ┌────────────────┐  ┌─────────────────┐  ┌───────────────┐   │  │
│  │  │ GetTransaction │  │ UpdateTransaction│ │DeleteTransaction│  │  │
│  │  └────────────────┘  └─────────────────┘  └───────────────┘   │  │
│  └───────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                           DTOs                                │  │
│  │  ┌──────────────────┐  ┌──────────────────┐                   │  │
│  │  │ CreateTransactionDTO│ │TransactionResponseDTO│              │  │
│  │  └──────────────────┘  └──────────────────┘                   │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          DOMAIN LAYER                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                         Entities                              │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  Transaction (id, description, amount, type, date)      │  │  │
│  │  │  TransactionType (INCOME, EXPENSE)                      │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Repository Interfaces                      │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │           TransactionRepositoryInterface                │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Django Implementation                      │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  TransactionModel (Django ORM)                          │  │  │
│  │  │  DjangoTransactionRepository                            │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│                    ┌─────────────────┐                              │
│                    │     SQLite      │                              │
│                    └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────────┘
```

### Camadas da Arquitetura

#### Presentation Layer

Responsável pela interface com o mundo externo através da API REST.

| Componente | Descrição |
|------------|-----------|
| **Views** | Controladores que recebem requisições HTTP e delegam para os Use Cases |
| **Serializers** | Validação e serialização de dados de entrada/saída |
| **URLs** | Roteamento de endpoints da API |

#### Application Layer

Contém a lógica de orquestração da aplicação.

| Componente | Descrição |
|------------|-----------|
| **Use Cases** | Casos de uso que implementam as regras de negócio da aplicação |
| **DTOs** | Objetos de transferência de dados entre camadas |

#### Domain Layer

O núcleo da aplicação, contendo as regras de negócio puras.

| Componente | Descrição |
|------------|-----------|
| **Entities** | Entidades de domínio com regras de validação internas |
| **Repository Interfaces** | Contratos abstratos para persistência de dados |

#### Infrastructure Layer

Implementações concretas de serviços externos e frameworks.

| Componente | Descrição |
|------------|-----------|
| **Models** | Modelos Django ORM para persistência |
| **Repositories** | Implementação concreta do repositório usando Django ORM |

### Benefícios da Arquitetura

| Benefício | Descrição |
|-----------|-----------|
| **Independência de Framework** | O domínio não possui dependências do Django |
| **Testabilidade** | Cada camada pode ser testada isoladamente |
| **Manutenibilidade** | Alterações em uma camada não afetam as demais |
| **Flexibilidade** | Permite substituição de implementações sem impacto no domínio |

---

## Tecnologias

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.10+ | Linguagem de programação |
| Django | 5.0+ | Framework web |
| Django REST Framework | 3.14+ | Toolkit para construção de APIs REST |
| SQLite | - | Sistema de gerenciamento de banco de dados |
| pytest | 7.0+ | Framework de testes |

---

## Estrutura do Projeto

```
iupi/
├── config/                          # Configurações do Django
│   ├── settings.py                  # Configurações principais
│   ├── urls.py                      # URLs raiz do projeto
│   └── wsgi.py                      # Configuração WSGI
│
├── src/                             # Código fonte da aplicação
│   ├── domain/                      # CAMADA DE DOMÍNIO
│   │   ├── entities/
│   │   │   └── transaction.py       # Entidade Transaction + TransactionType
│   │   └── repositories/
│   │       └── transaction_repository.py  # Interface do repositório
│   │
│   ├── application/                 # CAMADA DE APLICAÇÃO
│   │   ├── dtos/
│   │   │   └── transaction_dto.py   # DTOs de transação
│   │   └── use_cases/
│   │       ├── create_transaction.py
│   │       ├── get_transaction.py
│   │       ├── list_transactions.py
│   │       ├── update_transaction.py
│   │       ├── delete_transaction.py
│   │       └── get_summary.py
│   │
│   ├── infrastructure/              # CAMADA DE INFRAESTRUTURA
│   │   └── django_app/
│   │       ├── models/
│   │       │   └── transaction_model.py
│   │       ├── repositories/
│   │       │   └── django_transaction_repository.py
│   │       └── migrations/
│   │
│   └── presentation/                # CAMADA DE APRESENTAÇÃO
│       └── api/
│           └── v1/
│               ├── views/
│               │   └── transaction_views.py
│               ├── serializers/
│               │   └── transaction_serializer.py
│               └── urls/
│                   └── transaction_urls.py
│
├── manage.py                        # CLI do Django
├── requirements.txt                 # Dependências Python
└── db.sqlite3                       # Banco de dados SQLite
```

---

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Configuração do Ambiente

1. **Clone o repositório**
```bash
git clone https://github.com/MatheusSRMO/venha-estagiar-na-iupi-backend.git
cd venha-estagiar-na-iupi-backend
```

2. **Crie e ative um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações do banco de dados**
```bash
python manage.py migrate
```

5. **Inicie o servidor de desenvolvimento**
```bash
python manage.py runserver
```

A API estará disponível em `http://localhost:8000/api/v1/`

---

## Endpoints da API

### Base URL
```
http://localhost:8000/api/v1/
```

### Transações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/transactions/` | Criar nova transação |
| `GET` | `/transactions/` | Listar transações (com filtros opcionais) |
| `GET` | `/transactions/{id}/` | Obter transação por ID |
| `PUT` | `/transactions/{id}/` | Atualização completa de transação |
| `PATCH` | `/transactions/{id}/` | Atualização parcial de transação |
| `DELETE` | `/transactions/{id}/` | Remover transação |

### Resumo Financeiro

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/summary/` | Obter resumo financeiro agregado |

### Modelo de Dados: Transaction

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único (gerado automaticamente) |
| `description` | string | Descrição da transação |
| `amount` | decimal | Valor da transação (deve ser positivo) |
| `type` | string | Tipo da transação: `income` ou `expense` |
| `date` | date | Data da transação no formato `YYYY-MM-DD` |

### Parâmetros de Query (Listagem)

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `description` | string | Filtro por descrição (busca parcial, case-insensitive) |
| `type` | string | Filtro por tipo (`income` ou `expense`) |
| `page` | integer | Número da página para paginação |
| `size` | integer | Quantidade de itens por página |

---

## Exemplos de Uso

### Criar Transação

```bash
curl -X POST http://localhost:8000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Salário",
    "amount": 5000.00,
    "type": "income",
    "date": "2025-01-15"
  }'
```

**Resposta (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "description": "Salário",
  "amount": "5000.00",
  "type": "income",
  "date": "2025-01-15"
}
```

### Listar Transações

```bash
# Listar todas as transações
curl http://localhost:8000/api/v1/transactions/

# Aplicar filtro por tipo
curl http://localhost:8000/api/v1/transactions/?type=expense

# Aplicar filtro por descrição
curl http://localhost:8000/api/v1/transactions/?description=sal

# Combinar múltiplos filtros
curl http://localhost:8000/api/v1/transactions/?type=expense&description=cafe

# Paginação
curl http://localhost:8000/api/v1/transactions/?page=1&size=10
```

### Obter Transação por ID

```bash
curl http://localhost:8000/api/v1/transactions/550e8400-e29b-41d4-a716-446655440000/
```

### Atualizar Transação

```bash
curl -X PUT http://localhost:8000/api/v1/transactions/550e8400-e29b-41d4-a716-446655440000/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Salário atualizado",
    "amount": 5500.00,
    "type": "income",
    "date": "2025-01-15"
  }'
```

### Remover Transação

```bash
curl -X DELETE http://localhost:8000/api/v1/transactions/550e8400-e29b-41d4-a716-446655440000/
```

### Obter Resumo Financeiro

```bash
curl http://localhost:8000/api/v1/summary/
```

**Resposta (200 OK):**
```json
{
  "total_income": "15000.00",
  "total_expense": "4500.00",
  "net_balance": "10500.00"
}
```

---

## Testes

Para executar a suíte de testes:

```bash
pytest
```

Para executar com cobertura de código:

```bash
pytest --cov=src
```

---

## Autor

**Matheus Souza Ribeiro**

GitHub: [MatheusSRMO](https://github.com/MatheusSRMO)

---

## Licença

Este projeto foi desenvolvido como parte do processo seletivo para estágio na IUPI.

-----
## 💎 Requisitos de Qualidade de Código

* **1. Padrões de Nomenclatura:**
    * **Se usar nossa stack (Python/Django):**
        * Use `snake_case` para variáveis, funções, métodos e nomes de arquivos.
        * Use `PascalCase` para classes.
    * **Se usar outra stack:** Siga as convenções de nomenclatura dessa linguagem. O importante é a consistência.
        * **Exemplo (JavaScript/Node.js):** Use `camelCase` para variáveis e funções, `PascalCase` para classes e `kebab-case` para nomes de arquivos.
        * **Exemplo (Java/Spring):** Use `camelCase` para variáveis e métodos, e `PascalCase` para classes e interfaces.

* **2. Documentação de Código (Comentários):**
    * Use `docstrings` (para Python) ou o formato de documentação padrão da sua linguagem (JSDoc, JavaDoc, etc.) para documentar suas classes e funções/métodos principais.

* **3. Estrutura de Projeto:**
    * Você deve organizar seu código de forma lógica e escalável. A forma como você estrutura seus arquivos e módulos (separação de responsabilidades) será avaliada.

* **4. `.gitignore`:**
    * Configure seu `.gitignore` corretamente para ignorar arquivos desnecessários (ex: `__pycache__`, `node_modules/`, `.env`, `db.sqlite3`, `venv/`).

-----

## ⭐ Requisitos Bônus (Opcional)

  * **Paginação:** Adicione paginação à sua lista de `GET /transactions/`.
  * **Testes Automatizados:** Escreva testes unitários para sua API usando o framework de testes do Django.
  * **Autenticação JWT:**
    * 1\.  Criar um endpoint `POST /login/` que retorna um token (JWT).
    * 2\.  Proteger os endpoints de transações (só acessíveis com `Authorization: Bearer <token>`).
    * 3\.  A API deve retornar apenas transações do usuário autenticado.

-----

## 🚀 Como Testar sua API

Para testar os endpoints de uma API (enviar `POST`, `PUT`, etc.), você não usa o navegador. Recomendamos o uso de uma ferramenta como o **Postman** ou **Insomnia**. Elas facilitam o envio de requisições e a visualização das respostas.

## 📚 Materiais de Aprendizado (Pode consultar\!)
  * **Aprenda com vídeos**
    * [Como criar uma API em Django - Criando um CRUD - Aula Completa](https://youtu.be/Q2tEqNfgIXM?si=KBBw_cqHJ75b181a)

  * **Django (Fundamentos):**
      * [Guia de Instalação Rápida](https://docs.djangoproject.com/pt-br/5.2/intro/install/)
      * [Tutorial Oficial do Django](https://docs.djangoproject.com/pt-br/5.2/intro/tutorial01/)
      * [Documentação Oficial do Django](https://docs.djangoproject.com/pt-br/5.2/)
  * **Django REST Framework (Documentação):**
      * [Página Inicial da Documentação do DRF](https://www.django-rest-framework.org/)
      * [DRF - Serializers (Serialização)](https://www.django-rest-framework.org/tutorial/1-serialization/)
      * [DRF - ViewSets & Routers (Views)](https://www.django-rest-framework.org/api-guide/viewsets/)
      * [DRF - Filtering (Filtros)](https://www.django-rest-framework.org/api-guide/filtering/)
  * **Geral (Conceitos):**
      * [O que é uma API REST? (Guia da AWS)](https://aws.amazon.com/pt/what-is/restful-api/)
      * [HTTP Status Codes (MDN)](https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status)
  * **Ferramentas de Teste de API:**
      * [O que é o Postman? (Guia para Iniciantes)](https://learning.postman.com/docs/getting-started/introduction/)
  * **Autenticação:**
      * [DRF Simple JWT (Biblioteca popular)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
      * [DRF - Autenticação (Documentação)](https://www.django-rest-framework.org/api-guide/authentication/)

## 🚚 Como Entregar

1.  Faça um Fork deste repositório.
2.  Crie uma nova branch (ex: `meu-nome-desafio`).
3.  Faça seus commits.
4.  **IMPORTANTE:** Adicione ou atualize o `README.md` do seu projeto explicando:
      * A stack que você usou.
      * Como instalar as dependências.
      * Como preparar o banco de dados (rodar migrações, etc.).
      * Como rodar o projeto.
5.  Ao finalizar, abra um **Pull Request (PR)** do seu fork de volta para este repositório original.
6.  No corpo do PR, deixe comentários sobre suas decisões, dificuldades e o que você mais gostou.

Boa sorte\!
