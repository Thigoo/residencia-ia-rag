from pathlib import Path
from docling.document_converter import DocumentConverter
import os

os.environ["TORCHDYNAMO_DISABLE"] = "1"

pdf_dir = Path("docs/files")
output_dir = Path("docs/markdown")

output_dir.mkdir(parents=True, exist_ok=True)

converter = DocumentConverter()

for file in pdf_dir.glob("*.pdf"):
    print(f"Convertendo {file.name}")

    result = converter.convert(str(file))

    output_file = output_dir / f"{file.stem}.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result.document.export_to_markdown())

    print(f"Arquivo salvo em {output_file.resolve()}")

print("Conversão concluída!")