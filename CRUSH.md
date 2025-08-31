# CRUSH.md

Build/lint/test
- Install: pip install -r requirements.txt
- Run: python main.py --help
- Tests: pytest -q
- Single test file: pytest -q path/to/test_file.py
- Single test node: pytest -q path/to/test_file.py::TestClass::test_case
- Coverage: pytest -q --cov
- Lint: flake8 .
- Format: black .

Conventions
- Language: Python 3.8+; keep code compatible with Windows
- Imports: stdlib, third-party, local; absolute imports; no wildcard; group with blank lines
- Typing: from typing import Optional, Dict, List, Tuple, Union; prefer type hints everywhere; dataclasses where appropriate
- Naming: snake_case for functions/vars, PascalCase for classes, UPPER_SNAKE for constants; file names snake_case
- Errors: raise specific exceptions from core/exceptions.py; never swallow; add context; log via logging module
- Logging: use logging.getLogger(__name__); no prints; respect LOG_LEVEL env
- Requests: use requests with timeouts; retry per config; do not log secrets
- JSON: prefer utils/json_parser.RobustJSONParser for LLM outputs
- Providers: subclass providers/base_provider.BaseLLMProvider; register in core/llm_manager.LLMManager
- Actions: validate inputs; use ActionExecutor for execution; avoid hard-coded sleeps, respect config
- Screenshots: use ScreenshotManager; enable caching/optimization flags from env
- Config: read via config.py; allow overrides via CLI flags in main.py
- Style: run black; ensure flake8 passes; keep functions small; avoid comments that duplicate code; docstrings for public APIs
- Testing: pytest; use tmp paths; mark network-dependent tests and skip by default; seed randomness

Notes
- No Cursor or Copilot rules present
- Add .crush directory to .gitignore