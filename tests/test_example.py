import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentic import APP_NAME, __version__
from agentic.cli import main


def test_cli_output_uses_package_metadata(capsys):
    main()

    assert capsys.readouterr().out.strip() == f"Running {APP_NAME} CLI v{__version__}..."
