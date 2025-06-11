---

````markdown
# Comunitu - Plataforma para Cursos e Comunidades

O **Comunitu** é uma plataforma tudo-em-um desenvolvida para criadores, instrutores e comunidades que desejam oferecer **cursos online**, gerenciar **comunidades privadas ou públicas**, criar **eventos ao vivo**, e monetizar seus espaços com **planos pagos**.

Este projeto segue uma arquitetura moderna, modular e escalável, utilizando o ecossistema Django com renderização server-side, HTMX para interatividade e Tailwind CSS para estilização rápida e responsiva.

## 🖥️ **Tecnologias Utilizadas**

- **Python 3.12**: Linguagem principal.
- **Django 5.1**: Framework web back-end.
- **HTMX + django-htmx**: Interatividade sem SPA.
- **Tailwind CSS + Flowbite**: Estilo utilitário + componentes UI.
- **PostgreSQL**: Banco de dados relacional.
- **Cloudinary**: Armazenamento de mídia (vídeo, imagem, PDF).
- **Stripe**: Integração de pagamentos.
- **Docker + Docker Compose**: Ambientes isolados e deploy simplificado.

---

## 🚀 **Como executar o projeto localmente**

### 1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/comunitu.git
````

### 2. Acesse a pasta do projeto:

```bash
cd comunitu
```

### 3. Crie o ambiente virtual:

Utilize o [`uv`](https://github.com/astral-sh/uv) para instalação rápida de dependências Python:

```bash
uv install
source .venv/bin/activate
```

### 4. Crie um `.env` baseado no `.env.example`

### 5. Execute as migrações:

```bash
python manage.py migrate
```

### 6. Crie um superusuário:

```bash
python manage.py createsuperuser
```

### 7. (Opcional) Popule o banco com dados fake:

```bash
python manage.py loaddata apps/core/fixtures/*.json
```

> ⚠️ Não execute isso em produção.

### 8. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

---

## 🌟 **Funcionalidades (MVP)**

* 📚 Gerenciamento de cursos com seções e lições
* ✅ Rastreamento de progresso do aluno
* 👥 Autenticação de usuários e perfis (aluno/instrutor)
* 💳 Preparação para planos pagos com Stripe
* 🖼️ Página pública com apresentação e planos
* 🎥 Suporte a vídeos, PDFs, links embed e arquivos
* 🧩 Modular e expansível para eventos e comunidade

---

## 🔗 **Deploy**

O Comunitu é preparado para ser deployado em **VPS com Docker Compose**.
Você pode usar serviços como **Render, Railway, DigitalOcean ou AWS EC2**.

> Em produção, recomendamos o uso de [Gunicorn](https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/gunicorn/) + NGINX.

---

## 📁 **Estrutura do Projeto (resumo)**

```
comunitu/
├── apps/
│   ├── users/            # Autenticação, perfis, papéis
│   ├── courses/          # Cursos, seções, lições, progresso
│   ├── payments/         # Integração com Stripe
│   ├── core/             # Configurações globais, menus, landing
│   └── shared/           # Helpers reutilizáveis (utils, mixins)
├── config/               # Configuração geral do projeto Django
├── templates/            # Templates HTML com Tailwind + HTMX
├── static/               # JS, CSS compilado
├── docker/               # Dockerfiles e configs
├── .env, .dockerignore   # Configs do ambiente
```

---

## 📝 **Licença**

Este projeto está licenciado sob a [Licença MIT](LICENSE).
Uso livre para modificação e distribuição com atribuição ao autor original.

---

Se você quiser ajuda para configurar, implantar ou expandir o projeto, estou à disposição. 🚀

```

---

## ✅ Próximos passos possíveis:
- Gerar o **logo e favicon para Comunitu**
- Gerar o **projeto base Django com esses arquivos**
- Criar o repositório base para começar a codar

```
