## 🧭 **Guidelines de Engenharia (Engineering Guidelines)**

Este guia define os padrões e boas práticas a serem seguidos pela equipe de engenharia para garantir consistência, escalabilidade e qualidade no projeto.

---

### 1. 🏗️ Estrutura de Projeto Django

```bash
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

### 2. 📏 Convenções de Código

#### Python/Django

* Código formatado com **Black**
* Imports organizados com **isort**
* Linters: **flake8** ou **ruff**
* Nomes de campos e métodos em **snake\_case**
* Tabelas com nomes no plural (`courses`, `users`, etc.)
* Models com `Meta: ordering` e `__str__` implementado
* UUIDField como padrão para chaves primárias

#### Templates (HTMX + Tailwind)

* Componentes com **Flowbite**
* Lógica mínima em templates: usar `inclusion_tags` ou `context processors`
* Organização por página/tela (ex: `templates/courses/detail.html`)

---

### 3. 🧪 Testes

| Tipo                   | Ferramenta               | Cobertura mínima        |
| ---------------------- | ------------------------ | ----------------------- |
| Unitários              | `pytest + pytest-django` | 80%                     |
| Integração             | `pytest`                 | Rotas, views principais |
| E2E (quando aplicável) | Cypress (futuro)         | Fluxo de cursos e login |

* Criar testes para **cada model, view e formulário**
* Testes de integração para progresso do aluno e fluxo de publicação de curso

---

### 4. 🧵 Git / Versionamento

* **Convencional Commits** (`feat:`, `fix:`, `chore:` etc.)
* Nome de branches:

  * `feature/courses-create`
  * `bugfix/auth-redirect`
  * `release/v0.1.0`
* Pull Requests com:

  * Descrição do problema
  * Mudanças aplicadas
  * Checklist de testes feitos

---

### 5. 📚 Documentação e Comunicação

* Toda nova feature deve incluir:

  * Docstring nos métodos públicos
  * Esboço de uso (como criar curso, como funciona progress tracking)
* Issues no GitHub/GitLab com label por tipo: `bug`, `feature`, `refactor`

---

### 6. 💡 Performance e Escalabilidade

* **Querysets otimizados** com `select_related`, `prefetch_related`
* Paginação em listagens grandes (cursos, alunos)
* Armazenamento de arquivos em Cloudinary via link, nunca local
* Middleware leve, cache configurado via Redis (futuro)
