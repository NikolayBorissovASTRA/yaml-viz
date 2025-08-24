#!/bin/bash
set -e

export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

uv run streamlit run src/app.py
