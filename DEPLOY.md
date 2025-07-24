# 🚀 DEPLOY - Quiz LGPD Universidade Belz

## ✨ OPÇÕES DE DEPLOY GRATUITO

### 1. 🥇 RENDER.COM (Recomendado - 100% Gratuito)

**Passos:**

1. **Criar conta:** https://render.com (login com GitHub)

2. **Configurar no Render:**
   - New → Web Service
   - Connect Repository (conectar este projeto)
   - Settings:
     - **Build Command:** `pip install -r requirements_deploy.txt`
     - **Start Command:** `gunicorn app:app`
     - **Environment:** Python 3.11.0

3. **Deploy automático:** Render fará deploy automaticamente!

4. **URL pública:** Render fornecerá uma URL como `https://quiz-lgpd-belz.onrender.com`

**Vantagens Render:**
- ✅ Totalmente gratuito
- ✅ HTTPS automático
- ✅ Deploy automático via GitHub
- ✅ Sempre online (não hiberna)
- ✅ Fácil de configurar

---

### 2. 🥈 RAILWAY.APP (Alternativa)

**Passos:**
1. Acesse https://railway.app
2. Login com GitHub
3. Deploy from GitHub repo
4. Selecione este projeto
5. Deploy automático!

---

### 3. 🥉 HEROKU (Pago desde 2022)

❌ **Não recomendado** - Heroku removeu o plano gratuito

---

## 📁 ARQUIVOS PREPARADOS PARA DEPLOY

✅ `requirements_deploy.txt` - Dependências para produção
✅ `runtime.txt` - Versão do Python
✅ `Procfile` - Comando para iniciar app
✅ `app.py` - Configurado para produção
✅ `.gitignore` - Arquivos ignorados pelo Git

## 🔧 CONFIGURAÇÕES APLICADAS

- **Porta dinâmica:** App usa variável de ambiente `PORT`
- **Debug desabilitado:** Em produção
- **Gunicorn:** Servidor WSGI para produção
- **Sessões seguras:** Cookies HTTP-only
- **Arquivos estáticos:** Servidos pelo Flask

## 📊 MONITORAMENTO

Após deploy, o Quiz ficará disponível 24/7 para toda equipe da Universidade Belz!

**Funcionalidades online:**
- ✅ 14 participantes cadastrados
- ✅ 10 perguntas LGPD
- ✅ Timer 60 segundos
- ✅ Ranking em tempo real
- ✅ Estatísticas automáticas
- ✅ Design responsivo

## 🔗 PRÓXIMOS PASSOS

1. **Fazer upload para GitHub** (se ainda não estiver)
2. **Conectar no Render.com**
3. **Configurar deploy**
4. **Compartilhar URL com a equipe**
5. **Monitorar uso e rankings**

## ⚡ DEPLOY RÁPIDO (5 minutos)

```bash
# 1. Git (se necessário)
git init
git add .
git commit -m "Quiz LGPD pronto para deploy"
git push origin main

# 2. Render.com
# - Conectar repositório
# - Build: pip install -r requirements_deploy.txt  
# - Start: gunicorn app:app
# - Deploy!
```

**Resultado:** Quiz online em minutos! 🎉
