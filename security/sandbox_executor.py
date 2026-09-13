import multiprocessing

class SandboxExecutor:
    @staticmethod
    def rodar_seguro(funcao, *args):
        """Roda uma função em um processo isolado."""
        processo = multiprocessing.Process(target=funcao, args=args)
        processo.start()
        processo.join(timeout=10) # Tempo máximo de execução
        if processo.is_alive():
            processo.terminate()
            return "TIMEOUT_OU_FALHA"
        return "SUCESSO"