#!/bin/bash

# Simple wrapper script for notebook compilation
# Usage: ./scripts/render_notebooks.sh [notebook_name]

set -e

if [ $# -gt 0 ]; then
    echo "🚀 Compiling specific notebook: $1"
    uv run python scripts/compile_notebooks.py --notebook "$1"
else
    echo "🚀 Compiling all notebooks..."
    uv run python scripts/compile_notebooks.py --clean
fi

echo "📊 Compilation complete!"
echo "📖 To build Zola site: cd zdocs && zola build"
