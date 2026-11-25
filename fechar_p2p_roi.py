import hashlib
import inspect
import json
from datetime import datetime, timezone
from pathlib import Path

from core.super_retorno_financeiro import C2SovereignROIEngine
from core.visagismo_estetica_roi import VisagismoEsteticaRoi


def sha256_arquivo(caminho: Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def chamar_metodo_pdf(obj, nomes_metodos: list[str], caminho_pdf: Path) -> dict:
    for nome in nomes_metodos:
        fn = getattr(obj, nome, None)
        if callable(fn):
            sig = inspect.signature(fn)
            params = [
                p for p in sig.parameters.values()
                if p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
            ]
            try:
                if params:
                    resultado = fn(**{params[0].name: str(caminho_pdf)})
                else:
                    resultado = fn()
                pdf_real = Path(str(resultado)) if isinstance(resultado, str) and resultado.endswith(".pdf") and Path(resultado).exists() else caminho_pdf
                if pdf_real.exists():
                    return {
                        "metodo": nome,
                        "arquivo": str(pdf_real),
                        "tamanho_bytes": pdf_real.stat().st_size,
                        "sha256": sha256_arquivo(pdf_real),
                    }
                return {"metodo": nome, "arquivo": None, "erro": "PDF não encontrado após execução"}
            except Exception as exc:
                return {"metodo": nome, "arquivo": None, "erro": f"{type(exc).__name__}: {exc}"}
    return {"metodo": None, "arquivo": None, "erro": "Nenhum método de PDF encontrado"}


def testar_super_retorno(pasta: Path) -> list[dict]:
    cenarios = [
        ("base", {"ceo_name": "Executivo Base", "net_worth_eur": 1500000.0, "horizon_years": 5}),
        ("alto_patrimonio", {"ceo_name": "Executivo UHNW", "net_worth_eur": 12000000.0, "horizon_years": 15}),
    ]
    resultados = []
    for nome, kwargs in cenarios:
        sig = inspect.signature(C2SovereignROIEngine.__init__)
        validos = {k: v for k, v in kwargs.items() if k in sig.parameters}
        motor = C2SovereignROIEngine(**validos)
        pdf_out = pasta / f"super_retorno_{nome}.pdf"
        pdf_info = chamar_metodo_pdf(motor, ["gerar_pdf", "gerar_dossie", "gerar_relatorio"], pdf_out)
        resultados.append({
            "motor": "C2SovereignROIEngine",
            "cenario": nome,
            "parametros_aplicados": validos,
            "pdf": pdf_info,
        })
    return resultados


def testar_visagismo_roi(pasta: Path) -> list[dict]:
    cenarios = [
        ("base", {"nome_cliente": "Cliente Base", "fator_estresse": 0.25}),
        ("alto_estresse", {"nome_cliente": "Cliente Critico", "fator_estresse": 0.85}),
    ]
    resultados = []
    for nome, kwargs in cenarios:
        sig = inspect.signature(VisagismoEsteticaRoi.__init__)
        validos = {k: v for k, v in kwargs.items() if k in sig.parameters}
        motor = VisagismoEsteticaRoi(**validos)
        pdf_out = pasta / f"visagismo_roi_{nome}.pdf"
        pdf_info = chamar_metodo_pdf(
            motor,
            ["gerar_pdf_visagismo_roi", "gerar_pdf", "gerar_dossie", "gerar_relatorio"],
            pdf_out,
        )
        resultados.append({
            "motor": "VisagismoEsteticaRoi",
            "cenario": nome,
            "parametros_aplicados": validos,
            "pdf": pdf_info,
        })
    return resultados


def main() -> None:
    pasta = Path("evidencias_p2p_roi")
    pasta.mkdir(exist_ok=True)

    dados = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "super_retorno_financeiro": testar_super_retorno(pasta),
        "visagismo_estetica_roi": testar_visagismo_roi(pasta),
    }

    out_json = pasta / "fechamento_roi.json"
    out_json.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Fechamento de ROI salvo em: {out_json}")
    for grupo in ("super_retorno_financeiro", "visagismo_estetica_roi"):
        for item in dados[grupo]:
            pdf = item["pdf"]
            status = pdf["arquivo"] if pdf.get("arquivo") else pdf.get("erro")
            print(f"- {item['motor']} [{item['cenario']}]: {status}")


if __name__ == "__main__":
    main()