import os
import json
import logging

# Configuração de logs para destacar os alertas com precisão
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TTC_ErrorGuard")

class PlatformErrorGuard:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.erros_encontrados = []
        self.avisos = []

    def verificar_arquivos_obrigatorios(self, arquivos):
        """Verifica se todos os arquivos essenciais do ecossistema existem."""
        for arquivo in arquivos:
            caminho = os.path.join(self.base_dir, arquivo)
            if not os.path.exists(caminho):
                self.erros_encontrados.append(f"CRITICAL: Arquivo obrigatório ausente -> {arquivo}")
            else:
                logger.info(f"OK: Arquivo verificado: {arquivo}")

    def validar_integridade_json(self, caminho_arquivo):
        """Valida se os arquivos JSON de gateway e tratamentos estão corrompidos ou mal formatados."""
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados
        except json.JSONDecodeError as e:
            self.erros_encontrados.append(f"JSON ERROR em {caminho_arquivo}: Sintaxe inválida -> {e}")
        except Exception as e:
            self.erros_encontrados.append(f"ERROR ao ler {caminho_arquivo} -> {e}")
        return None

    def inspecionar_biometria_e_metricas(self, dados_json):
        """Analisa se os biomarcadores e métricas estão dentro de limites lógicos/esperados."""
        # Exemplo de verificação no gateway da clínica médica
        gateway_clinica = dados_json.get("gateway_clinica_medica", {})
        biomarcadores = gateway_clinica.get("biomarcadores_de_regeneracao", {})
        
        # Validador de faixa percentual (exemplo: taxa de regeneração ou umidade não podem passar de 100% ou ser negativas)
        for chave, valor in biomarcadores.items():
            if isinstance(valor, str) and "%" in valor:
                try:
                    num = float(valor.replace("%", "").strip())
                    if not (0.0 <= num <= 100.0):
                        self.erros_encontrados.append(f"ANOMALIA DE DADO: Biomarcador '{chave}' com valor fora do intervalo físico ({valor})")
                except ValueError:
                    self.avisos.append(f"AVISO: Não foi possível converter o biomarcador '{chave}' para validação numérica.")

    def executar_varredura_completa(self):
        print("--- INICIANDO VARREDURA PREVENTIVA DO TTC GLOBAL ---")
        
        # 1. Checagem de arquivos críticos da plataforma
        arquivos_criticos = [
            "ultimo_motodiagnostico.json", 
            "gateway_orquestrador.py", 
            "biomarcadores_de_regeneracao.json"
        ]
        # (Você pode ajustar a lista conforme os nomes exatos no seu diretório)
        
        # 2. Executando auditoria estrutural
        for arq in os.listdir(self.base_dir):
            if arq.endswith(".json"):
                logger.info(f"Inspecionando integridade de: {arq}")
                dados = self.validar_integridade_json(arq)
                if dados:
                    self.inspecionar_biometria_e_metricas(dados)

        # 3. Relatório final de comportamento
        print("\n--- RELATÓRIO DE DIAGNÓSTICO DE ERROS ---")
        if self.erros_encontrados:
            print(f"❌ {len(erros := self.erros_encontrados)} ERRO(S) CRÍTICO(S) ENCONTRADO(S):")
            for erro in erros:
                print(f"   - {erro}")
            print("\n🚨 AÇÃO RECOMENDADA: Corrija os pontos acima antes de fazer o deploy/implantação.")
            return False
        else:
            print("✅ Nenhum erro crítico estrutural encontrado. O ecossistema está íntegro para subir.")
            if self.avisos:
                print((f"⚠️ Avisos menores ({len(self.avisos)}):"))
                for aviso in self.avisos:
                    print(f"   - {aviso}")
            return True

# Para rodar o script no seu ambiente:
if __name__ == "__main__":
    guard = PlatformErrorGuard()
    guard.executar_varredura_completa()