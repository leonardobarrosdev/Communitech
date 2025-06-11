## ⚙️ **Documento de Decisões Técnicas (Technical Decisions Doc)**

Este documento descreve as escolhas arquiteturais e tecnológicas feitas no projeto, com justificativas, implicações e alternativas consideradas.

---

### 1. 🔧 **Stack de Tecnologia**

| Camada         | Tecnologia                     | Justificativa                                                        |
| -------------- | ------------------------------ | -------------------------------------------------------------------- |
| Backend        | Django 5.1 + Python 3.12       | Framework robusto, produtivo e escalável com ORM maduro              |
| Frontend       | HTMX + django-htmx             | Permite SPA-like UX sem overhead de JS frameworks                    |
| Estilização    | Tailwind CSS + django-tailwind | Utilitário moderno e customizável, integração fluida com componentes |
| UI Components  | Flowbite                       | Conjunto pronto e responsivo de componentes para Tailwind            |
| Banco de Dados | PostgreSQL                     | Banco relacional poderoso com suporte a JSON, escalável              |
| Mídia          | Cloudinary                     | Armazenamento e entrega otimizada de arquivos e vídeos               |
| Pagamento      | Stripe                         | Gateway robusto, internacional, ideal para SaaS                      |

---

### 2. 📦 **Arquitetura de Aplicação**

| Elemento                     | Decisão                                                                       |
| ---------------------------- | ----------------------------------------------------------------------------- |
| Estrutura modular de apps    | Cada domínio (ex: `courses`, `users`, `payments`) será um app Django separado |
| UUIDs como primary key       | Segurança e escalabilidade, evitando IDs preditivos                           |
| Admin separado do front      | Interface administrativa Django desativada para o público                     |
| HTMX para interatividade     | Ajax progressivo com baixa fricção e controle direto do servidor              |
| Docker para ambiente         | Containers separados para `web`, `db`, `nginx`, `celery` no futuro            |
| Assets compilados (Tailwind) | Uso de build automático via PostCSS dentro do Django Tailwind                 |

---

### 3. 🔐 **Segurança**

| Área              | Decisão                                               |
| ----------------- | ----------------------------------------------------- |
| Autenticação      | Django `AbstractUser` customizado com papéis (`role`) |
| Proteção de rotas | Decoradores + middleware baseado em grupo/perfil      |
| Hash de senhas    | Padrão Django (`PBKDF2`)                              |
| Rate limit/login  | Reforço via middleware futuro (ex: `django-axes`)     |
| Uploads de mídia  | Apenas via Cloudinary com validação no backend        |

---

### 4. ⚙️ **Alternativas Consideradas**

| Área             | Escolha Final | Alternativas      | Justificativa                                      |
| ---------------- | ------------- | ----------------- | -------------------------------------------------- |
| Frontend         | HTMX          | React, Vue        | Tempo de desenvolvimento reduzido, foco no backend |
| Pagamento        | Stripe        | Paypal, PagSeguro | Melhor suporte técnico e documentação              |
| Storage de mídia | Cloudinary    | AWS S3            | Setup mais simples, CDN embutido                   |

---

### 5. 🌍 **Internacionalização**

* A aplicação será inicialmente em **português**.
* Estrutura do projeto preparada para i18n com `gettext` para futuras traduções.
