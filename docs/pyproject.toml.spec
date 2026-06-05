# pyproject.toml SPEC (Track 2 Red 진입 시 생성)

Red Gate **G5** 충족용 템플릿. **SPEC 단계에서는 파일을 만들지 않음** — Red 진입 Day 1에 Agent에게 생성 요청.

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "unit-converter"
version = "0.1.0"
description = "Length unit converter — OCP/SRP refactor (workshop PRD)"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "PyYAML>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[project.scripts]
unit-converter = "unit_converter.app.cli:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["unit_converter*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["unit_converter"]
omit = ["unit_converter/app/cli.py"]
```

**생성 후:**

```bash
pip install -e ".[dev]"
pytest --collect-only -q   # 0 tests until Red TC added
```
