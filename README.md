
# 🤖 Runrun.it Excel Agent

Este projeto gera automaticamente um relatório em Excel com todos os comentários feitos no Runrun.it no **dia anterior**, e envia esse arquivo para o seu Telegram.

## 📁 Estrutura do projeto

```
runrun-excel-agent/
├── .github/workflows/runrun-agent.yml  # Workflow para rodar diariamente
├── runrun_excel_agent_env.py           # Script principal
├── requirements.txt                    # Dependências
├── README.md                           # Este arquivo
└── .gitignore                          # Ignora .env e arquivos temporários
```

## 🔐 Configuração de GitHub Secrets

Acesse: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Crie os seguintes segredos:

- `RUNRUN_APP_KEY`
- `RUNRUN_USER_TOKEN`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## 🚀 Rodando localmente (opcional)

```bash
pip install -r requirements.txt
python runrun_excel_agent_env.py
```

## ☁️ Agendamento automático

O script roda todos os dias às **7:30 da manhã (BRT)** graças ao GitHub Actions.
