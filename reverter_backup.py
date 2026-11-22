from pathlib import Path
import shutil

RAIZ = Path(r"C:\projetos python\THIERRY_TECHNOLOGY_CORE\THIERRY_TECH_CORE_2026")
BACKUP = RAIZ / "_backup_seguro"

if not BACKUP.exists():
  print("Pasta _backup_seguro não encontrada.")
else:
  restaurados = 0
  for arq_bkp in BACKUP.rglob("*"):
    if arq_bkp.is_file():
      destino = RAIZ / arq_bkp.relative_to(BACKUP)
      destino.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(arq_bkp, destino)
      restaurados += 1
  print(f"Restaurados {restaurados} arquivo(s) a partir de _backup_seguro.")