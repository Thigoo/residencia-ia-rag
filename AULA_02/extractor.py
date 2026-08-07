from pathlib import Path
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

class PaperMetadata(BaseModel):
    titulo: str
    autores: list[str]
    ano: int

def read_markdown(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

modelo = os.getenv("OPENAI_MODEL", "openrouter/free")

input_dir = Path("AULA_02/output")

for md_file in input_dir.glob("*.md"):
    print(f"Processando {md_file.name}...")

    markdown = read_markdown(md_file)

    response = client.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role": "system",   
                "content": """
Você extrai metadados de artigos científicos.

Responda SOMENTE um JSON válido neste formato:

{
    "titulo": "Título",
    "autores": ["Autor 1", "Autor 2"],
    "ano": 2024
}

Se não conseguir identificar o ano, utilize 0.
""",
            },
            {
                "role": "user",
                "content": markdown,
            },
        ],
        temperature=0,
    )

    json_text = response.choices[0].message.content

    metadata = PaperMetadata.model_validate_json(json_text)

    output_file = input_dir / f"output_{md_file.stem}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            metadata.model_dump(),
            f,
            indent=4,
            ensure_ascii=False,
        )

    print(f"✔ {output_file.name} salvo.")

print("Todos os arquivos foram processados.")