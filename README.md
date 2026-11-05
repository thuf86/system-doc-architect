<p align="center">
  <code>==================== S Y S T E M  D O C  A R C H I T E C T ====================</code><br>
  <b><i>Auditoria Documental & Documentação Técnica Corporativa em Português</i></b><br><br>
  <img src="https://img.shields.io/badge/Version-1.0-green?style=for-the-badge&logo=github">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Claude%20Code-Supported-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Language-PT--BR-yellow?style=for-the-badge">
</p>

---

## ⭐ Apoie o Projeto

Caso o System Doc Architect seja útil para seu ambiente de desenvolvimento ou auditoria, considere deixar uma estrela no repositório.

---

# 📘 System Documentation Architect

**System Documentation Architect** é uma skill em português brasileiro para auditar sistemas existentes e produzir documentação técnica corporativa com evidências, módulos em Markdown/PDF e documento mestre.

A skill instrui o agente a investigar o projeto em modo somente leitura; os scripts incluídos fazem inventário estático, geração de PDF a partir de Markdown e validação heurística. Os scripts **não substituem** a análise técnica do agente nem garantem descoberta completa de arquitetura.

**Autor:** Romildo — [@thuf86](https://github.com/thuf86)  
🌐 **Website:** https://medium.com/@romildothuf

---

## 📌 Visão Geral

Diferente de um gerador genérico de README, o System Doc Architect foi desenvolvido para criar um pacote documental estruturado a partir de evidências do código e dos manifests do sistema.

O projeto oferece:

* Contrato operacional claro para auditoria, documentação completa ou atualização
* Inventário estático do repositório analisado
* Guias por domínio (arquitetura, APIs, dados, infra, segurança, negócio/QA)
* Template padronizado de módulos documentais
* Geração de PDF a partir dos Markdown
* Validação heurística da saída
* Fluxo pensado para Claude Code (e reutilizável em outros agentes compatíveis com skills)

---

## ✨ Principais Recursos

* 🧾 Documentação técnica corporativa em **PT-BR**
* 🔍 Modos `auditoria`, `completo` e `atualizacao`
* 🧱 Até **10 módulos** aplicáveis + documento mestre
* 🏷️ Marcação de evidência: `[CONFIRMADO]`, `[INFERIDO]`, `[NÃO VERIFICADO]`
* 📊 Diagramas Mermaid/PlantUML apenas com entidades sustentadas por evidência
* 🐍 Scripts Python para inventário, PDF e validação
* 🪟 Compatível com Windows (caminhos absolutos)
* 🐧 Compatível com Linux
* 🔐 Análise somente leitura por padrão, com exclusão de segredos no inventário
* 🧪 Smoke tests básicos incluídos

---

## 🗂️ Estrutura do Projeto

```text
system-doc-architect/
├── SKILL.md                      # Contrato operacional da skill
├── README.md
├── requirements.txt              # Dependências opcionais (PDF / testes)
├── .gitignore
├── assets/
│   └── module-template.md        # Modelo de módulo documental
├── references/
│   ├── architecture.md
│   ├── business-quality.md
│   ├── data-apis.md
│   ├── evidence.md
│   ├── infrastructure.md
│   ├── modules.md
│   ├── security.md
│   └── standards.md
├── scripts/
│   ├── inventory.py              # Inventário estático do projeto
│   ├── build_documents.py        # Markdown → PDF
│   └── validate_output.py        # Validação heurística da saída
└── tests/
    └── test_smoke.py
```

---

## ⚙️ Requisitos

* Python **3.10+**
* Git (para clonar o repositório)
* Claude Code (ou agente compatível com skills em `~/.claude/skills`)
* Opcional para PDF: `reportlab` (`python -m pip install -r requirements.txt`)
* Opcional para testes: `pytest`

### Windows

* Windows 10 ou superior
* PowerShell recomendado
* Caminhos absolutos para o projeto analisado (ex.: `C:\Projetos\Sistema`)

### Linux

* Distribuição compatível com Python 3.10+
* Bash

---

## 📦 Instalação

### Claude Code

Clone ou copie a pasta `system-doc-architect` para o diretório de skills:

```text
Windows:
%USERPROFILE%\.claude\skills\system-doc-architect

Linux / macOS:
~/.claude/skills/system-doc-architect
```

Exemplo:

```bash
git clone https://github.com/thuf86/system-doc-architect.git ~/.claude/skills/system-doc-architect
```

Reinicie o Claude Code ou inicie uma nova sessão.

### Dependências opcionais (PDF)

```bash
cd ~/.claude/skills/system-doc-architect
python -m pip install -r requirements.txt
```

---

## 🎛️ Uso no Claude Code

```text
/system-doc-architect completo /caminho/do/projeto
/system-doc-architect auditoria /caminho/do/projeto
/system-doc-architect atualizacao /caminho/do/projeto
```

Informe ao agente um **diretório de saída separado** do repositório analisado, sempre que possível.

| Modo | Resultado esperado |
| ---- | ------------------ |
| **completo** | Inventário, módulos `01`–`10` aplicáveis, `00_documento_mestre.md`, PDFs e validação |
| **auditoria** | `00_auditoria.md` + inventário |
| **atualizacao** | Diff documental, `CHANGELOG_DOCUMENTACAO.md`, módulos afetados e mestre regenerado |

---

## 🛠️ Ferramentas Manuais

Os scripts podem ser executados isoladamente, mas **não produzem documentação técnica completa** sem a análise do agente.

```bash
python scripts/inventory.py --root /projeto --out /saida/inventory.json
python scripts/build_documents.py --input /saida --output /saida/pdf
python scripts/validate_output.py --dir /saida --mode completo
```

---

## 🧱 Saída Padrão

```text
<diretorio-saida>/
├── inventory.json
├── 00_documento_mestre.md      # ou 00_auditoria.md
├── 01_....md … 10_....md
├── pdf/
├── validation_report.json
└── CHANGELOG_DOCUMENTACAO.md   # modo atualizacao
```

---

## 🛡️ Segurança

* A análise é **somente leitura** por padrão
* O inventário exclui diretórios de segredos e arquivos ocultos sensíveis
* Não copie `.env`, certificados privados, dumps ou tokens para a documentação
* Revise toda saída antes de compartilhar
* A validação é heurística e **não** substitui revisão de segurança ou visual

---

## 📚 Referências Incluídas

| Arquivo | Domínio |
| ------- | ------- |
| `references/architecture.md` | Arquitetura de software |
| `references/data-apis.md` | Dados e APIs |
| `references/infrastructure.md` | Infra / DevOps / SRE |
| `references/security.md` | AppSec e compliance |
| `references/business-quality.md` | Negócio e QA |
| `references/modules.md` | Catálogo dos 10 módulos |
| `references/standards.md` | Padrões de redação |
| `references/evidence.md` | Regras de evidência |

---

## 🙏 Créditos

Skill criada e mantida por **Romildo (Thuf)** — [@thuf86](https://github.com/thuf86).

Contribuições e feedbacks são bem-vindos via issues e pull requests.
