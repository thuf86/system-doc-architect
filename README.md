# System Documentation Architect

Skill em português brasileiro para auditoria documental e geração de documentação técnica de sistemas existentes. A skill instrui o agente a investigar o projeto; os scripts fazem inventário estático, geração de PDF a partir de Markdown e validação básica. Os scripts **não substituem** análise técnica nem garantem descoberta completa de arquitetura.

## Estrutura

```
system-doc-architect/
├── SKILL.md                 # Contrato operacional da skill
├── README.md
├── requirements.txt         # Dependências opcionais (PDF)
├── assets/                  # Templates de módulo
├── references/              # Guias por domínio
├── scripts/                 # Inventário, PDF e validação
└── tests/                   # Smoke tests
```

## Instalação (Claude Code)

Clone ou copie a pasta `system-doc-architect` para `~/.claude/skills/` (Windows: `%USERPROFILE%\.claude\skills\`). Reinicie o Claude Code ou inicie uma nova sessão.

Requer Python 3.10+. Para PDF:

```bash
python -m pip install -r requirements.txt
```

## Uso

```
/system-doc-architect completo /caminho/do/projeto
/system-doc-architect auditoria /caminho/do/projeto
/system-doc-architect atualizacao /caminho/do/projeto
```

Informe um diretório de saída separado do repositório, se possível. Em Windows use caminho absoluto (ex.: `C:\Projetos\Sistema`).

## Ferramentas manuais

```bash
python scripts/inventory.py --root /projeto --out /saida/inventory.json
python scripts/build_documents.py --input /saida --output /saida/pdf
python scripts/validate_output.py --dir /saida --mode completo
```

## Segurança

A análise é somente leitura por padrão. O inventário exclui diretórios de segredos e arquivos ocultos sensíveis, limita tamanho e não lê conteúdo de arquivos de código para a saída. Revise toda documentação gerada antes de compartilhar. A validação é heurística e não substitui revisão de segurança.

## Licença

Uso sob responsabilidade de quem publica a documentação gerada. Ajuste a licença do repositório conforme sua necessidade.
