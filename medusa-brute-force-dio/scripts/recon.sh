#!/usr/bin/env bash
# recon.sh - Reconhecimento rapido do alvo antes do brute force
# Uso: ./recon.sh 192.168.56.102

set -euo pipefail

TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
  echo "Uso: $0 <IP_DO_ALVO>"
  echo "Ex.: $0 192.168.56.102"
  exit 1
fi

echo "[*] Testando conectividade com $TARGET ..."
if ! ping -c 2 -W 2 "$TARGET" >/dev/null 2>&1; then
  echo "[!] Alvo nao respondeu ao ping. Verifique a rede host-only."
  exit 1
fi
echo "[+] Alvo acessivel."

echo "[*] Varrendo servicos do laboratorio (FTP/HTTP/SMB) ..."
nmap -p 21,80,139,445 -sV "$TARGET"

echo
echo "[*] Enumerando usuarios SMB (pode levar alguns segundos) ..."
nmap --script smb-enum-users -p 445 "$TARGET" || true

echo
echo "[+] Reconhecimento concluido."
