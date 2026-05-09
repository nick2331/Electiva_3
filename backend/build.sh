#!/usr/bin/env bash
set -e

# Instala dependencias del sistema para WeasyPrint (si el entorno lo permite)
if command -v apt-get &>/dev/null; then
  apt-get update -qq && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf2.0-0 \
    libffi-dev libgl1 libglib2.0-0 2>/dev/null || true
fi

pip install --upgrade pip
pip install -r requirements.txt
