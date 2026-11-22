# -*- coding: utf-8 -*-
"""
===========================================================================
THIERRY TECHNOLOGY CONCEPT GLOBAL © 2026 | ALL RIGHTS RESERVED
MIBO SOVEREIGN INTELLIGENCE FRAMEWORK - SENTINEL ZERO-TRUST ENGINE
===========================================================================
"""

import os
import sys
import json
import hashlib
import platform
from datetime import datetime

class TTCSentinel:
    def __init__(self, license_filename="zero_trust.enc", audit_log="security/sentinel_forensic.log", tokens_db="registro_tokens_ativos_monaco.json"):
        self.license_filename = license_filename
        self.audit_log = audit_log
        self.tokens_db = tokens_db
        
        # Garante a existência da pasta de segurança
        os.makedirs(os.path.dirname(self.audit_log), exist_ok=True)
        
        # Estado Operacional e de Sessão
        self.session_active = False
        self.service_finished = False
        self.current_operator = "DESCONHECIDO"
        self.current_client_context = None
        self.last_screen_accessed = "INICIO"
        
        # Cronologia e Rastreio inicializados com segurança
        self.start_time = None
        self.end_service_time = None
        self.last_activity_time = None
        self.action_history = []
        
        # Executa barreira de hardware Zero-Trust no carregamento imediato
        if not self._verify_hardware_trust():
            self.hardware_bloqueado = True
        else:
            self.hardware_bloqueado = False

    def _get_hardware_fingerprint(self):
        """Gera a assinatura imutável baseada no hardware profundo da máquina."""
        raw_data = f"{platform.processor()}-{platform.machine()}-{platform.node()}"
        return hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

    def _verify_hardware_trust(self):
        """Valida se a licença bate com o hardware ou se é necessário iniciar o fluxo de migração."""
        current_hw = self._get_hardware_fingerprint()

        if not os.path.exists(self.license_filename):
            # Primeiro boot sem arquivo local - aguarda preenchimento do modal corporativo
            return False
        else:
            try:
                with open(self.license_filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("hardware_signature") == current_hw
            except Exception:
                return False

    def processar_migracao_nó_autonoma(self, nome_responsavel: str, nome_empresa: str, email_compra: str, token_licenca: str, aceite_termos: bool) -> dict:
        """
        Executa a migração automática de hardware: valida os dados, registra o carimbo temporal 
        (data, mês, ano e hora), atualiza o banco global e revoga o HWID antigo.
        """
        if not aceite_termos:
            return {
                "sucesso": False,
                "mensagem": "Você deve aceitar os Termos de Licenciamento Global para prosseguir."
            }

        if not all([nome_responsavel, nome_empresa, email_compra, token_licenca]):
            return {
                "sucesso": False,
                "mensagem": "Todos os campos corporativos são obrigatórios para a validação."
            }

        current_hw = self._get_hardware_fingerprint()
        timestamp_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Carrega o banco de tokens ativos do licenca.py se existir
        banco_tokens = {"tokens_ativos": {}, "total_vagas_ocupadas": 0}
        if os.path.exists(self.tokens_db):
            try:
                with open(self.tokens_db, "r", encoding="utf-8") as f:
                    banco_tokens = json.load(f)
            except Exception:
                pass

        token_encontrado = None
        # Procura o token informado ou o e-mail correspondente no banco de dados corporativo
        if token_licenca in banco_tokens["tokens_ativos"]:
            token_encontrado = token_licenca
        else:
            # Varre buscando pelo e-mail caso o token exato não tenha sido digitado
            for t_key, t_val in banco_tokens["tokens_ativos"].items():
                if t_val.get("titular", "").lower() == email_compra.strip().lower() or email_compra.strip().lower() in t_key.lower():
                    token_encontrado = t_key
                    break

        # Se houver banco de tokens configurado, atualiza a lista de nós (removendo antigos e inserindo o novo)
        if token_encontrado and token_encontrado in banco_tokens["tokens_ativos"]:
            dados_t = banco_tokens["tokens_ativos"][token_encontrado]
            nos_registrados = dados_t.get("nos_registrados", [])
            limite_nos = dados_t.get("nos_permitidos", 2)
            
            # Remove qualquer registro prévio deste exato HWID para evitar duplicidade
            nos_registrados = [n for n in nos_registrados if n.get("hwid") != current_hw]
            
            # Se estourou o limite de nós, faz a substituição inteligente do nó mais antigo (migração automática)
            if len(nos_registrados) >= limite_nos:
                no_removido = nos_registrados.pop(0)
                self._log_forensic_event("NODE_REVOKED_BY_MIGRATION", f"Nó anterior revogado automaticamente: {no_removido.get('hwid')}")

            # Adiciona o novo nó corporativo
            novo_registro_no = {
                "hwid": current_hw,
                "responsavel": nome_responsavel.strip(),
                "empresa": nome_empresa.strip(),
                "email": email_compra.strip().lower(),
                "data_migracao": timestamp_atual,
                "lat": None,
                "lon": None
            }
            nos_registrados.append(novo_registro_no)
            banco_tokens["tokens_ativos"][token_encontrado]["nos_registrados"] = nos_registrados
            
            # Salva o banco atualizado de forma atômica
            try:
                temp_db = self.tokens_db + ".tmp"
                with open(temp_db, "w", encoding="utf-8") as f:
                    json.dump(banco_tokens, f, indent=4, ensure_ascii=False)
                os.replace(temp_db, self.tokens_db)
            except Exception as e:
                return {"sucesso": False, "mensagem": f"Erro ao atualizar o registro de tokens: {str(e)}"}

        # Gera o cofre local de confiança (`zero_trust.enc`) para este novo computador
        license_data = {
            "hardware_signature": current_hw,
            "company_name": nome_empresa.strip(),
            "owner_name": nome_responsavel.strip(),
            "owner_email": email_compra.strip().lower(),
            "migrated_at": timestamp_atual,
            "status": "SECURE_BOUND_ACTIVE"
        }
        
        try:
            with open(self.license_filename, "w", encoding="utf-8") as f:
                json.dump(license_data, f, ensure_ascii=False, indent=4)
            
            self.hardware_bloqueado = False
            self._log_forensic_event("CLIENT_AUTONOMOUS_MIGRATION", {
                "empresa": nome_empresa,
                "responsavel": nome_responsavel,
                "email": email_compra,
                "timestamp": timestamp_atual
            })
            
            return {
                "sucesso": True,
                "mensagem": f"Licença migrada com sucesso para este computador em {timestamp_atual}! Acesso liberado."
            }
        except Exception as e:
            return {
                "sucesso": False,
                "mensagem": f"Falha ao gerar cofre de segurança local: {str(e)}"
            }

    def check_system_health(self):
        """Verifica ociosidade perigosa com blindagem contra valores nulos."""
        if not self.session_active or self.last_activity_time is None:
            return "OK"

        idle_time = (datetime.now() - self.last_activity_time).total_seconds()
        
        if self.service_finished and idle_time > 180:
            self._trigger_kill_switch(
                "EXPOSICAO_OCIOSA_RISCO", 
                f"O sistema permaneceu exposto por mais de 3 minutos após o fim do atendimento."
            )
        
        return "OK"

    def _trigger_kill_switch(self, violation_code, description):
        """Encerra a execução em caso de violação de segurança."""
        dossier = {
            "VIOLATION_CODE": violation_code,
            "TIMESTAMP": datetime.now().isoformat(),
            "OPERATOR_IN_CHARGE": self.current_operator,
            "DESCRIPTION": description,
            "SYSTEM_STATE": "TERMINATED_BY_SENTINEL"
        }

        report_path = "security/SECURITY_BREACH_REPORT.json"
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(dossier, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

        self._log_forensic_event("KILL_SWITCH_ACTIVATED", dossier)
        print(f"\n🚨 [TTC SENTINEL - BLOQUEIO DE SEGURANÇA ATIVO] 🚨\nMOTIVO: {description}")
        sys.exit(99)

    def _log_forensic_event(self, event_type, details):
        """Grava log de auditoria forense."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "details": details
        }
        try:
            with open(self.audit_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass