# 📝 Tarefas do Projeto Comunitu – Plataforma de Comunidade e Aprendizagem

---

## 🔐 Autenticação e Usuários
- [x] Criar modelo customizado de usuário (`User` com `AbstractUser`)
- [x] Registro de usuários
- [x] Login via DRF
- [x] Logout com expiração de token
- [x] Middleware de proteção para rotas privadas
- [ ] Painel de perfil do usuário (API)
- [ ] Atribuição de papéis (admin, moderador, membro)

---

## 🧱 Comunidade & Espaços
- [ ] Modelos: `Community`, `Space`, `Group`, `Membership`
- [ ] Organização de espaços (público, privado, secreto)
- [ ] Associações entre espaços e membros
- [ ] Permissões de acesso por espaço
- [ ] Posts e comentários com threads
- [ ] Moderação (excluir conteúdo, banir usuários)

---

## 📚 Cursos
- [x] Models: `Course`, `Section`, `Lesson`, `Progress`
- [x] Serializers: lista de cursos, detalhes, lição
- [x] Views: listagem, detalhes, criação
- [x] Marcar lição como concluída
- [ ] API para curso estruturado/agendado
- [ ] Conteúdos com mídia (PDF, vídeo, embed)
- [ ] Integração com IA para gerar conteúdo (LangChain)

---

## 📅 Eventos e Transmissões
- [ ] Modelos: `Event`, `RSVP`
- [ ] Agendamento de eventos com descrição e data
- [ ] Confirmação de presença (RSVP)
- [ ] Envio de lembretes por e-mail
- [ ] Integração com ferramentas externas (Zoom, Jitsi)

---

## 💬 Mensagens e Comunicação
- [ ] Mensagens diretas entre membros
- [ ] Chat por espaço (em threads)
- [ ] Endpoint de status online/offline (futuro)
- [ ] Notificações simples (digest, alertas)

---

## 💳 Pagamentos (Stripe)
- [x] Criar produtos e planos no Stripe Dashboard
- [x] Integração com `stripe.checkout`
- [x] Webhook para conceder acesso
- [ ] Controle de acesso por plano (espaços/cursos pagos)
- [ ] Criação de cupons e múltiplos planos
- [ ] Histórico de assinaturas e cancelamentos

---

## 🧠 Integração com IA (LangChain)
- [ ] Criar app `ai`
- [ ] Conectar LangChain à API
- [ ] Registrar chave de API por instrutor (OpenAI, Gemini, etc.)
- [ ] Geração de conteúdos via IA (ex: texto de lições)
- [ ] Logs de uso da IA por usuário
- [ ] Controle de acesso (premium / uso pessoal)

---

## 🎨 Personalização e Branding
- [ ] Upload de logo e banner da comunidade
- [ ] Escolha de cores do tema
- [ ] Menus personalizados
- [ ] Uso de domínio próprio

---

## ✉️ E-mail e Notificações
- [ ] Envio de notificações por e-mail (eventos, cursos)
- [ ] Digest semanal automatizado
- [ ] Anúncios manuais por administradores
- [ ] Integração SMTP (SendGrid, SES, etc.)

---

## 🔧 Infraestrutura e Deploy
- [ ] Estrutura inicial com Docker Compose (`api`, `db`, `nginx`)
- [x] Configuração de ambientes (`.env`, `environ`)
- [ ] Dockerfile de produção
- [ ] Deploy em VPS (Ubuntu, NGINX, Gunicorn)
- [ ] Script de deploy manual
- [ ] HTTPS com Let's Encrypt (`certbot`)
- [ ] Backup do banco (cronjob)
- [ ] Logs e health-check

---

## 🧪 Testes e Qualidade
- [x] Setup do Pytest
- [x] Cobertura mínima de 80% nos módulos core
- [x] Testes para views, modelos e permissões
- [x] Linting com `flake8`
- [x] Formatação com `black`
