import requests
import ast
from urllib.parse import urljoin
from pathlib import Path
from shutil import copyfileobj
from black import format_file_contents, FileMode

def download(base_url: str, download_dir: Path, filename: str) -> Path:
    """
    Downloads a file specified by a base URL and filename to the specified download directory
    """
    download_path = download_dir / filename
    if download_path.exists():
        print(f"Skipping download of {download_path}")
    else:
        url = urljoin(base_url, filename)
        download_path.parent.mkdir(parents=True, exist_ok=True)
        with download_path.open("w") as fp:
            response = requests.get(url, stream=True)
            fp.write(response.text)

    return download_path

def make_compact(dir: Path) -> None:
    manifest = requests.get("https://w3c.github.io/json-ld-api/tests/compact-manifest.jsonld").json()
    tests: list[ast.expr] = []
    for test in manifest["sequence"]:

        base_url = manifest["baseIri"]
        kwargs: list[ast.keyword] = []

        if "expect" in test:
            cls = "PositiveCompactTest"
            download(base_url, dir, test["expect"])
            kwargs.append(ast.keyword(
                "expect", ast.Constant(test["expect"])
            ))
        elif "expectErrorCode" in test:
            cls = "NegativeCompactTest"
            kwargs.append(ast.keyword(
                "expect_error_code", ast.Constant(test["expectErrorCode"])
            ))
        else:
            raise Exception()

        if (context := test.get("context")) is not None:
            download(base_url, dir, context)
            kwargs.append(ast.keyword(
                "context", ast.Constant(context)
            ))

        download(base_url, dir, test["input"])

        tests.append(
            ast.Call(
                func=ast.Name(cls),
                keywords=[
                    ast.keyword(
                        arg="name",
                        value=ast.Constant(test["name"])
                    ),
                    ast.keyword(
                        arg="purpose",
                        value=ast.Constant(test["purpose"])
                    ),
                    ast.keyword(
                        arg="input",
                        value=ast.Constant(test["input"])
                    ),
                    *kwargs
                ]
            )
        )

    ret = ast.Module(body=[
        ast.ImportFrom("json_ld_test.model", [
            ast.alias("PositiveCompactTest"),
            ast.alias("NegativeCompactTest"),
            ast.alias("ContextTestCase"),
        ], 0),
        ast.AnnAssign(
            target=ast.Name("tests"),
            value=ast.List(elts=tests),
            annotation=ast.Subscript(ast.Name("list"), ast.Name("ContextTestCase")),
            simple=1
        )
    ])

    python = dir / "compact.py"
    with python.open("w") as fp:
        fp.write(format_file_contents(ast.unparse(ast.fix_missing_locations(ret)), fast=False, mode=FileMode()))

def main():
    root = Path("src/json_ld_test")
    make_compact(root)

if __name__ == "__main__":
    main()