import argparse
import os
import sys

from dotenv import load_dotenv


def configure_graphviz_runtime():
    if os.name != "nt" or not hasattr(os, "add_dll_directory"):
        return

    candidate_dirs = [
        os.getenv("GRAPHVIZ_BIN"),
        r"C:\Program Files\Graphviz\bin",
        r"C:\Program Files (x86)\Graphviz\bin",
    ]

    for path in candidate_dirs:
        if path and os.path.isdir(path):
            os.add_dll_directory(path)
            if path not in os.environ.get("PATH", ""):
                os.environ["PATH"] = path + os.pathsep + os.environ.get("PATH", "")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gera DER com ERAlchemy2 a partir da string de conexao no .env"
    )
    parser.add_argument(
        "--env-key",
        default="DB_CONNECTION",
        help="Nome da variavel de ambiente com a URL SQLAlchemy do banco (padrao: DB_CONNECTION)",
    )
    parser.add_argument(
        "--output",
        default="docs/der_armazem.png",
        help="Arquivo de saida (.png, .svg, .pdf, .dot, etc)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    load_dotenv()
    configure_graphviz_runtime()

    from eralchemy2 import render_er

    connection = os.getenv(args.env_key)
    if not connection:
        print(
            f"Erro: variavel de ambiente '{args.env_key}' nao encontrada no .env.",
            file=sys.stderr,
        )
        sys.exit(1)

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        render_er(connection, args.output)
    except Exception as exc:
        print(f"Falha ao gerar DER: {exc}", file=sys.stderr)
        print(
            "Dica: para formatos de imagem, instale o Graphviz no sistema e adicione no PATH.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"DER gerado com sucesso em: {args.output}")


if __name__ == "__main__":
    main()
