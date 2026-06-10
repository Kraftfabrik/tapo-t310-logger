#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

venv_dir="$project_dir/.venv"
python_bin="$venv_dir/bin/python"

requirements_file="$project_dir/requirements.txt"
script="$project_dir/tapo_t310_logger.py"

cd "$project_dir"

if [[ ! -d "$venv_dir" ]]; then
    python3 -m venv "$venv_dir"
fi

if ! "$python_bin" -c "import kasa" >/dev/null 2>&1; then
    "$python_bin" -m pip install --quiet --upgrade pip

    if [[ -f "$requirements_file" ]]; then
        "$python_bin" -m pip install --quiet -r "$requirements_file"
    else
        "$python_bin" -m pip install --quiet python-kasa
    fi
fi

exec "$python_bin" "$script"
