import requests
import ast
from urllib.parse import urljoin
from pathlib import Path
from shutil import copyfileobj

def make_compact(dir: Path) -> None:
    manifest = requests.get("https://w3c.github.io/json-ld-api/tests/compact-manifest.jsonld").json()
    tests: list[ast.expr] = []
    for test in manifest["sequence"]:

        base = manifest["baseIri"]
        args: list[ast.keyword] = []
        for field in ["input", "expect", "context"]:
            # Each field has a corresponding file
            if field in test:
                filename: str = test[field]
                download_path = dir / filename
                if download_path.exists():
                    print(f"Skipping download of {download_path}")
                else:
                    url = urljoin(base, filename)
                    download_path.parent.mkdir(parents=True, exist_ok=True)
                    with download_path.open("wb") as fp:
                        response = requests.get(url, stream=True)
                        copyfileobj(response.raw, fp)
                args.append(ast.keyword(
                    arg=field,
                    value=ast.Constant(filename)
                ))
        tests.append(
            ast.Call(
                func=ast.Name("ContextTestCase"),
                keywords=args
            )
        )

    ret = ast.Module(body=[
        ast.ImportFrom("json_ld_test.model", [
            ast.alias("ContextTestCase"),
        ], 0),
        ast.Assign(
            targets=[ast.Name("tests")],
            value=ast.List(elts=tests)
        )
    ])

    python = dir / "compact.py"
    with python.open("w") as fp:
        fp.write(ast.unparse(ast.fix_missing_locations(ret)))

def main():
    root = Path("src/json_ld_test")
    make_compact(root)

if __name__ == "__main__":
    main()