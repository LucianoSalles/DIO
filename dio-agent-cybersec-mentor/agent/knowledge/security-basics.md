# Fundamentos de segurança

Base de conceitos para o agente conduzir análises de segurança. É usada pela skill `skills/vulnerability-analysis/SKILL.md`.

## Vulnerabilidade, ameaça e risco

- **Vulnerabilidade:** uma fraqueza que pode ser explorada. Ex.: uma consulta SQL montada com o texto que o usuário digitou.
- **Ameaça:** quem ou o que pode explorar a fraqueza. Ex.: um atacante na internet, um script automatizado, um funcionário descontente.
- **Risco:** a chance de a ameaça explorar a vulnerabilidade, combinada com o estrago que isso causaria.

Analogia: a janela aberta é a vulnerabilidade, o ladrão é a ameaça, e o risco depende do bairro e do que há dentro da casa. Janela aberta em um cofre de banco é diferente de janela aberta em um galpão vazio. Por isso o contexto vem antes da avaliação.

Outros termos úteis:

- **Ativo:** o que tem valor e precisa de proteção (dados, sistema, servidor, conta).
- **Exploit:** o meio usado para explorar uma vulnerabilidade.
- **Superfície de ataque:** tudo o que está exposto e pode ser alcançado por um atacante.
- **Mitigação:** medida que reduz a probabilidade ou o impacto.
- **Risco residual:** o que sobra depois da mitigação. Nunca é zero.

## A tríade CID

Toda análise de impacto responde a três perguntas:

| Pilar | Pergunta | Exemplo de violação |
|-------|----------|---------------------|
| **Confidencialidade** | Alguém pode ver o que não deveria? | Vazamento da tabela de usuários |
| **Integridade** | Alguém pode alterar o que não deveria? | Mudança de saldo ou de senha de outra pessoa |
| **Disponibilidade** | O sistema pode parar de atender quem precisa? | Banco de dados apagado ou serviço derrubado |

Em inglês, a tríade aparece como CIA: Confidentiality, Integrity, Availability.

## Como medir o risco

Use sempre a mesma escala, para as análises serem comparáveis.

**Impacto** é a maior nota entre os três pilares da tríade:

| Nota | Significado |
|------|-------------|
| Baixo | Dano pequeno e fácil de reverter, sem dados sensíveis |
| Médio | Dano limitado a parte dos dados ou dos usuários, ou parada parcial |
| Alto | Dados sensíveis expostos ou alterados, controle do sistema ou parada total |

**Probabilidade** combina exposição e facilidade de exploração:

| Nota | Significado |
|------|-------------|
| Baixa | Só acessível localmente ou exige acesso privilegiado e muito conhecimento |
| Média | Acessível na rede interna ou por usuário autenticado, ou exige alguma condição específica |
| Alta | Acessível pela internet sem autenticação, com técnica conhecida e fácil de automatizar |

**Severidade** é o cruzamento das duas:

| Impacto \ Probabilidade | Baixa | Média | Alta |
|-------------------------|-------|-------|------|
| **Baixo** | Baixa | Baixa | Média |
| **Médio** | Baixa | Média | Alta |
| **Alto** | Média | Alta | Crítica |

Esta matriz é uma simplificação didática. No mercado, o padrão mais usado para pontuar vulnerabilidades é o CVSS (https://www.first.org/cvss/). Quando o estudante quiser se aprofundar, indique o CVSS como próximo passo.

## Referências para classificar

- **CWE** (https://cwe.mitre.org): catálogo de tipos de fraqueza. Responde "que tipo de erro é este?".
- **MITRE ATT&CK** (https://attack.mitre.org): catálogo de táticas e técnicas de atacantes. Responde "o que o atacante faz com isso?".
- **OWASP Top 10** (https://owasp.org/www-project-top-ten/): os riscos mais comuns em aplicações web.
- **CVE** (https://www.cve.org): identificador de uma vulnerabilidade específica em um produto específico.

Falhas comuns em laboratório e como classificá-las:

| Falha | CWE | Técnica do MITRE ATT&CK |
|-------|-----|-------------------------|
| SQL Injection | CWE-89 | T1190: Exploit Public-Facing Application |
| Injeção de comando do sistema | CWE-78 | T1190, seguida de T1059: Command and Scripting Interpreter |
| Cross-Site Scripting (XSS) | CWE-79 | T1189: Drive-by Compromise (quando usado para atingir visitantes) |
| Senha ou chave escrita no código | CWE-798 | T1552.001: Unsecured Credentials, Credentials In Files |
| Senha guardada em texto puro | CWE-256 | T1552: Unsecured Credentials |
| Login sem limite de tentativas | CWE-307 | T1110: Brute Force |
| Serviço remoto (SSH, RDP) exposto com senha fraca | CWE-521 | T1133: External Remote Services, com T1110 ou T1078: Valid Accounts |

Esta tabela não é completa. Se a falha não estiver aqui e você não tiver certeza do identificador, diga isso ao estudante e oriente a conferir na fonte. Nunca invente um identificador.

## Boas práticas

- **Nunca confie na entrada.** Tudo o que vem de fora (formulário, URL, arquivo, API) é dado, nunca comando. Valide e use consultas parametrizadas.
- **Menor privilégio.** Cada usuário, serviço e conta de banco tem só a permissão de que precisa.
- **Defesa em profundidade.** Uma camada falha, então use várias: validação, parametrização, permissões, monitoramento.
- **Reduza a superfície de ataque.** Feche portas, desative serviços e remova o que não é usado.
- **Segredos fora do código.** Senhas e chaves ficam em variáveis de ambiente ou cofres, nunca no repositório.
- **Senhas com hash e salt.** Nunca em texto puro. Use algoritmos próprios para senha, como Argon2, bcrypt, scrypt ou PBKDF2.
- **Atualize sempre.** Sistema, dependências e bibliotecas com correções de segurança em dia.
- **Autenticação forte.** Chaves em vez de senha no SSH, e segundo fator onde for possível.
- **Registre e monitore.** Sem log, não há como saber que algo aconteceu.
- **Tenha backup testado.** Backup que nunca foi restaurado é só uma esperança.
- **Erros discretos.** Mensagens de erro não devem revelar detalhes internos para o usuário.

## Ética e limites

Segurança ofensiva só se pratica com autorização. O agente analisa apenas código, servidores e contas do próprio estudante ou de laboratório. Testar sistemas de terceiros sem autorização é crime no Brasil (Lei nº 12.737/2012 e Art. 154-A do Código Penal). Na dúvida sobre a autorização, o agente não prossegue.
