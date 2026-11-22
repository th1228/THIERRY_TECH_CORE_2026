# DOSSIER TÉCNICO & ARQUITETURAL — TTC GLOBAL
**Projeto:** Thierry Technology Concept Global (Core Ecosystem)
**Padrão Visual:** High-End / All Black & Gold/Neon
**Objetivo:** Ecossistema Integrado de Visagism, Biometria, Osteometria e Blindagem Forense.

---

## 1. ESTADO ATUAL DO SISTEMA (As Is)
* **Arquitetura Operacional:** Execução centralizada via script principal na raiz, rodando localmente (ex: `127.0.0.1:801`) e encapsulado como App Nativo do Windows via atalho dedicado.
* **Interface:** Interface web otimizada para alta performance, integrada com módulos de varredura biométrica e geração de relatórios forenses.
* **Dependências & Limpeza:** Varredura e higienização de logs temporários (`.log`) e caches do Python (`__pycache__`) automatizadas via script de faxina (`faxina_ttc.py`).

---

## 2. ESTADO ALVO / ESTRUTURA IDEAL (To Be)
Para garantir total escalabilidade, facilidade de manutenção e organização para auditoria/registro de propriedade intelectual, a árvore de diretórios oficial segue o padrão modular:

```text
THIERRY_TECH_CORE_2026/
│
├── principal.py              # Ponto de entrada (Entrypoint) do sistema
├── __init__.py               # Inicializador do pacote raiz
├── faxina_ttc.py             # Script de manutenção e limpeza de logs/cache
│
├── core/                     # Módulos lógicos centrais
│   ├── __init__.py
│   ├── visagismo.py          # Regras de negócio de Visagismo & Métrica Facial
│   ├── biometria.py          # Rotinas de Biometria e Scanner
│   └── osteometria.py        # Módulos forenses e de simulação
│
├── assets/                   # Recursos estáticos e visuais (High-End)
│   └── logo.png
│
└── reports/                  # Diretório dedicado para salvamento de relatórios e PDFs