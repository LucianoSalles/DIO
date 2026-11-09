# 🛡️ DIO Agent: mentor de cibersegurança

> Evolução do [DIO Agent](https://github.com/digitalinnovationone/dio-agent) que analisa uma vulnerabilidade com você do jeito que um profissional de segurança faria: pergunta o contexto, avalia impacto, probabilidade e severidade e só então orienta a correção.

Projeto do Desafio de Projeto da [DIO](https://dio.me). Nenhum modelo foi treinado: o agente aprende só pelo que está escrito em arquivos Markdown.

---

## ⚠️ Aviso

Tudo aqui é educacional. O código em `lab/` é **propositalmente vulnerável**, usa um banco em memória e não deve ser usado em sistema real. A skill só analisa código e servidores do próprio estudante ou de laboratório. Testar sistemas de terceiros sem autorização é crime (Lei nº 12.737/2012 e Art. 154-A do Código Penal).

---

## 🎯 A especialização, e por quê

Se você pergunta a um chat genérico "como deixo meu servidor seguro?", ele devolve uma lista de comandos. Um profissional de segurança faz o contrário: primeiro quer saber **o que** é o servidor, **onde** ele está e **quem** o alcança, porque a mesma falha pode ser um detalhe em um laboratório e um desastre em produção.

Por isso especializei o agente em **análise de vulnerabilidades**. Com a skill, ele:

1. pergunta o contexto, uma pergunta por vez;
2. identifica a falha e classifica com CWE;
3. explica a exploração e cita a técnica do MITRE ATT&CK;
4. avalia impacto (confidencialidade, integridade, disponibilidade), probabilidade e severidade;
5. conduz a correção, da causa raiz à prática que resolve;
6. faz uma nova varredura para validar;
7. confirma o que o estudante aprendeu.

---

## 📁 O que foi criado e alterado

| Arquivo | Situação | O que é |
|---------|----------|---------|
| [`skills/vulnerability-analysis/SKILL.md`](skills/vulnerability-analysis/SKILL.md) | Novo | O roteiro que o agente segue, com as regras defensivas e o formato fixo da análise |
| [`skills/vulnerability-analysis/README.md`](skills/vulnerability-analysis/README.md) | Novo | A explicação da skill para pessoas |
| [`agent/knowledge/security-basics.md`](agent/knowledge/security-basics.md) | Novo | Vulnerabilidade, ameaça, risco, tríade CID, matriz de severidade, referências (CWE, ATT&CK) e boas práticas |
| [`agent/persona.md`](agent/persona.md) | Alterado | Seção "Quando o assunto é segurança" e dois limites novos |
| [`AGENTS.md`](AGENTS.md) | Alterado | Linha da skill na tabela, o arquivo novo na base de conhecimento e o limite "Segurança com responsabilidade" |
| [`lab/app.py`](lab/app.py) | Novo | Login vulnerável a SQL Injection, para o agente analisar |
| [`lab/app_fixed.py`](lab/app_fixed.py) | Novo | Login corrigido, com consulta parametrizada e senha com hash |
| [`lab/test_login.py`](lab/test_login.py) | Novo | Testes que provam a falha e a mitigação |
| [`lab/cenarios.md`](lab/cenarios.md) | Novo | Prompts de teste da skill, com o que conferir em cada um |

O restante (demais skills, `docs/` e `CLAUDE.md`) veio do repositório base, sem alteração.

---

## ✨ A melhoria escolhida: análise sempre no mesmo formato

Das ideias do desafio, escolhi **fazer a análise sair sempre no mesmo formato**. Toda análise termina com a mesma tabela:

| Critério | Nota |
|----------|------|
| Confidencialidade, Integridade, Disponibilidade | Baixo, Médio ou Alto |
| Impacto | o maior dos três |
| Probabilidade | Baixa, Média ou Alta |
| **Severidade** | Baixa, Média, Alta ou Crítica |

A severidade não é opinião do agente: ela sai de uma matriz de impacto por probabilidade, escrita em [`agent/knowledge/security-basics.md`](agent/knowledge/security-basics.md). Com isso dá para colocar duas análises lado a lado (o SQL Injection do `app.py` e um SSH mal configurado, por exemplo) e decidir o que corrigir primeiro.

Para exercitar o formato além do código, o [`lab/cenarios.md`](lab/cenarios.md) traz também um cenário de infraestrutura, um de configuração insegura e um de limite ético, em que o agente deve recusar.

---

## 🚀 Como rodar

### 1. Instale um harness

Nas Aulas foi usado o **Hermes**. Siga a instalação da documentação oficial: https://hermes-agent.nousresearch.com/docs

O agente segue o padrão aberto `AGENTS.md`, então também funciona em outros harnesses, como Claude Code, Codex, OpenCode e Google Antigravity.

### 2. Baixe o projeto

```bash
git clone https://github.com/LucianoSalles/DIO.git
```

```bash
cd DIO/dio-agent-cybersec-mentor
```

### 3. Abra o harness **dentro da pasta do projeto**

```bash
hermes
```

Este é o cuidado que pega muita gente: o terminal precisa estar na pasta que tem o `AGENTS.md`. Aberto em outro lugar, o agente não encontra os arquivos.

### 4. Converse

Análise do código vulnerável:

```
Atue como especialista em AppSec. Analise o arquivo lab/app.py, que é meu e de laboratório.
Encontre a falha, explique a exploração, cite a técnica do MITRE ATT&CK e me oriente na correção.
```

Nova varredura depois da correção:

```
Corrigi o login. Faça uma nova varredura no arquivo lab/app_fixed.py e me diga
se o SQL Injection foi mitigado e se sobrou algum risco.
```

Cenário de conversa, para conferir se ele pergunta antes de agir:

```
Tenho um servidor Ubuntu de laboratório exposto na internet. Como deixo ele seguro?
```

---

## 🧪 O laboratório

O `lab/app.py` monta o SQL juntando o que a pessoa digitou:

```python
query = (
    "SELECT id, usuario FROM usuarios "
    "WHERE usuario = '" + usuario + "' AND senha = '" + senha + "'"
)
```

Se alguém digita `admin' --` no usuário, o trecho da senha vira comentário e o login passa sem senha. É um SQL Injection (CWE-89), associado no MITRE ATT&CK à técnica T1190, Exploit Public-Facing Application.

O `lab/app_fixed.py` troca pela consulta parametrizada, em que a entrada vai como dado e nunca como comando:

```python
conn.execute(
    "SELECT id, usuario, salt, senha_hash FROM usuarios WHERE usuario = ?",
    (usuario,),
)
```

Ele também deixa de guardar a senha em texto puro e passa a usar hash com salt (PBKDF2).

Para provar a falha e a mitigação sem depender do agente, rode os testes. Só precisa de Python 3, sem instalar nada:

```bash
cd lab
```

```bash
python -m unittest -v test_login.py
```

Saída:

```
test_injecao_bloqueada (test_login.LoginCorrigido.test_injecao_bloqueada) ... ok
test_login_legitimo (test_login.LoginCorrigido.test_login_legitimo) ... ok
test_senha_errada (test_login.LoginCorrigido.test_senha_errada) ... ok
test_senha_nao_fica_em_texto_puro (test_login.LoginCorrigido.test_senha_nao_fica_em_texto_puro) ... ok
test_injecao_entra_sem_senha (test_login.LoginVulneravel.test_injecao_entra_sem_senha) ... ok
test_login_legitimo (test_login.LoginVulneravel.test_login_legitimo) ... ok

Ran 6 tests in 1.279s

OK
```

O teste `test_injecao_entra_sem_senha` passa porque a injeção **funciona** no código vulnerável. O `test_injecao_bloqueada` passa porque as mesmas entradas são **recusadas** no código corrigido.

---

## 📸 Evidências

Os prints das conversas com o agente ficam na pasta [`images/`](images/README.md), que lista o que capturar.

---

## 🗂️ Estrutura

```
dio-agent-cybersec-mentor/
├── README.md                        Este guia
├── AGENTS.md                        Definição do agente (lida pelo harness)
├── CLAUDE.md                        Atalho para o Claude Code
├── agent/
│   ├── persona.md                   Personalidade, com a postura de segurança
│   └── knowledge/
│       ├── security-basics.md       Fundamentos de segurança
│       ├── dio-platform.md          (base)
│       └── learning-experiences.md  (base)
├── skills/
│   ├── vulnerability-analysis/      A skill nova: SKILL.md e README.md
│   └── ...                          Skills do repositório base
├── lab/                             Código vulnerável, corrigido, testes e cenários
├── images/                          Evidências
└── docs/                            Glossário e guia do You.com (base)
```

---

## 🧩 Todas as skills do agente

| Skill | Para que serve | Experimente pedir |
|-------|----------------|-------------------|
| [Análise de vulnerabilidades](skills/vulnerability-analysis/SKILL.md) | Conduz uma análise de segurança com contexto, risco e correção | "Analise a segurança do meu lab/app.py." |
| [Plano de estudos](skills/study-plan/SKILL.md) | Organiza o que estudar, em que ordem e em quanto tempo | "Quero concluir este Bootcamp em 2 meses, me ajuda?" |
| [Destravar desafio](skills/unblock-challenge/SKILL.md) | Conduz você até a solução de um desafio, sem dar a resposta pronta | "Travei nesse desafio, me ajuda?" |
| [Explicar conceito](skills/explain-concept/SKILL.md) | Explica conceitos de forma simples, com analogias e exemplos | "Não entendi o que é uma API." |
| [Pesquisa na web](skills/web-search/SKILL.md) | Responde dúvidas atuais com fontes citadas | "Qual a versão estável do Node hoje?" |
| [Revisão de portfólio](skills/portfolio-review/SKILL.md) | Dá feedback sobre o seu portfólio e GitHub | "O que falta no meu GitHub para uma vaga júnior?" |
| [Caminho AI Builder](skills/ai-builder-path/SKILL.md) | Ajuda a escolher o próximo passo na Carreira AI Builder | "Qual Formação AI Builder combina comigo?" |

---

## 🙏 Créditos

Baseado no [DIO Agent](https://github.com/digitalinnovationone/dio-agent), da Digital Innovation One.
