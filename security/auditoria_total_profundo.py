import hashlib
import json
import os
from datetime import datetime


class AuditoriaTotalProfunda:

  def __init__(
      self,
      log_dir="Dado/Config",
      operator="Thiêrry (TCC SOBERANO)",
      tenant="TTC Global Corp",
  ):
    self.log_dir = log_dir
    self.operator = operator
    self.tenant = tenant
    os.makedirs(self.log_dir, exist_ok=True)
    self.master_ledger_path = os.path.join(
        self.log_dir, "master_audit_ledger_profundo.json"
    )

  def _gerar_hash_criptografico(self, payload_str):
    return hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

  def registrar_auditoria_profunda(
      self, modulo, acao, status="AUTORIZADO", metricas=None, detalhes=None
  ):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro = {
        "timestamp": timestamp,
        "operador": self.operator,
        "organizacao": self.tenant,
        "modulo_alvo": modulo,
        "operacao": acao,
        "status_execucao": status,
        "metricas_biometricas_ou_financeiras": metricas or {},
        "detalhes_contexto": detalhes or {},
    }

    payload_str = json.dumps(registro, sort_keys=True)
    registro["hash_integridade_sha256"] = self._gerar_hash_criptografico(
        payload_str
    )

    self._persistir_ledger(registro)
    self._espelhar_terminal(registro)
    return registro

  def _persistir_ledger(self, registro):
    historico = []
    if os.path.exists(self.master_ledger_path):
      try:
        with open(self.master_ledger_path, "r", encoding="utf-8") as f:
          historico = json.load(f)
      except Exception:
        historico = []

    historico.append(registro)

    with open(self.master_ledger_path, "w", encoding="utf-8") as f:
      json.dump(historico, f, indent=4, ensure_ascii=False)

  def _espelhar_terminal(self, registro):
    print("\n" + "=" * 60)
    print(" [TCC GLOBAL CORP] — ESPELHO DE AUDITORIA TOTAL & PROFUNDA ")
    print("=" * 60)
    print(f" Timestamp     : {registro['timestamp']}")
    print(f" Operador      : {registro['operador']}")
    print(f" Organização   : {registro['organizacao']}")
    print(f" Módulo Alvo   : {registro['modulo_alvo']}")
    print(f" Operação      : {registro['operacao']}")
    print(f" Status        : {registro['status_execucao']}")
    print(
        f" Métricas      : {json.dumps(registro['metricas_biometricas_ou_financeiras'], ensure_ascii=False)}"
    )
    print(
        f" Detalhes      : {json.dumps(registro['detalhes_contexto'], ensure_ascii=False)}"
    )
    print(f" Hash SHA-256  : {registro['hash_integridade_sha256']}")
    print("=" * 60 + "\n")

  def auditar_integridade_cadeia(self):
    if not os.path.exists(self.master_ledger_path):
      resultado = {"status": "VAZIO", "integridade": True}
      print(f"[AUDITORIA] Status da cadeia: {resultado}")
      return resultado

    with open(self.master_ledger_path, "r", encoding="utf-8") as f:
      historico = json.load(f)

    cadeia_integra = True
    for item in historico:
      hash_salvo = item.pop("hash_integridade_sha256", None)
      payload_str = json.dumps(item, sort_keys=True)
      hash_calculado = self._gerar_hash_criptografico(payload_str)
      item["hash_integridade_sha256"] = hash_salvo

      if hash_salvo != hash_calculado:
        cadeia_integra = False
        break

    resultado = {
        "total_registros_auditados": len(historico),
        "cadeia_imutavel": cadeia_integra,
        "ultima_verificacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    print(f"[AUDITORIA] Validação de Cadeia Imutável: {resultado}")
    return resultado


if __name__ == "__main__":
  auditor = AuditoriaTotalProfunda()
  auditor.registrar_auditoria_profunda(
      modulo="security.audit_ledger",
      acao="Varredura de Integridade Sênior & Espelho",
      status="SUCESSO",
      metricas={"frequencia_vetorial": "1.818 Hz", "niveis_governanca": "100%"},
      detalhes={"jurisdicao": "Monaco & Brasil", "tier": "Tier-1"},
  )
  auditor.auditar_integridade_cadeia()