# Comunitu - Platform to Courses and Communities

**comunitu-api** is an API for building an all-in-one platform designed for creators, instructors, and communities who want to offer **online courses**, manage **private or public communities**, host **live events**, and monetize their spaces with **paid plans**.

This project follows a modern, modular, and scalable architecture, leveraging the Django ecosystem with Django Rest Framework.

## 🖥️ **Technologies Useds**

- **Python 3.12**: Principal language.
- **Django 5.1**: Web back-end framework.
- **Django Rest Framework**: Rest API.
- **PostgreSQL**: Relational database.
- **Cloudinary**: Storage of media (video, imagem, PDF).
- **Stripe**: Payment integration.
- **Docker + Docker Compose**: Isolated environment and simplificated deploy.

---

## 🚀 **Runing local project**

### 1. Clone the repository:
```bash
git clone https://github.com/leonardobarrosdev/comunitu.git
````

### 2. Access the project diretory:

```bash
cd comunitu
```

### 3. Create a virtual environment:

Use the [`uv`](https://github.com/astral-sh/uv) for fast install of Python dependences:

```bash
uv install
source .venv/bin/activate
```

### 4. Create a `.env` based on `.env.example`

### 5. Execute the migrations:

```bash
python manage.py migrate
```

### 6. Create a superuser:

```bash
python manage.py createsuperuser
```

> ⚠️ Not execute this in production.

### 8. Init the development server:

```bash
python manage.py runserver
```

---

## 🌟 **Funtionalities (MVP)**

* 📚 Course management with sections and lessons
* ✅ Student progress tracking
* 👥 User and profile authentication (student/instructor)
* 💳 Preparation for paid plans with Stripe
* 🖼️ Public page with presentation and plans
* 🎥 Support for videos, PDFs, embed links, and files
* 🧩 Modular and expandable for events and communities

---

## 🔗 **Deploy**

Comunitu is ready to be deployed on a **VPS with Docker Compose**.
You can use services like **Render, Railway, DigitalOcean, or AWS EC2**.

> In production, we recommend use of [Gunicorn](https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/gunicorn/) + NGINX.

---

## 📁 **Project Structure (summary)**

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

## 📝 **Licese**

This project is licensed under the [MIT License](LICENSE).
Free to use, modify, and distribute with attribution.

---

If you need help setting up, deploying, or expanding your project, I'm here to help. 🚀

```

---

## ✅ Next prossible steps:
- Create user Auth using email or username (use this two options)

```
