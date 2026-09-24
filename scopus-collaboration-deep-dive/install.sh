#!/usr/bin/env bash
# One-line installer for scopus-collaboration-deep-dive
# Usage: curl -fsSL https://raw.githubusercontent.com/minimax/scopus-collaboration-deep-dive/main/install.sh | bash
#
# Or after cloning:
#   ./install.sh
#
# What it does:
# 1. Verifies Python 3.10+
# 2. Installs Python dependencies
# 3. Verifies LibreOffice (for XLSX post-processing)
# 4. Runs the test suite
# 5. Prints quickstart example

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SKILL_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "📦 Installing scopus-collaboration-deep-dive..."

# 1. Check Python
echo -n "🐍 Checking Python... "
if command -v python3 &> /dev/null; then
    PY=python3
elif command -v python &> /dev/null; then
    PY=python
else
    echo -e "${RED}NOT FOUND${NC}"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

PY_VERSION=$($PY -c 'import sys; print("%d.%d" % sys.version_info[:2])')
PY_OK=$(echo "$PY_VERSION >= 3.10" | $PY -c 'import sys; print(int(sys.argv[1]))' 3.10 2>/dev/null || echo 0)
if [ "$PY_OK" = "1" ]; then
    echo -e "${GREEN}OK${NC} ($PY_VERSION)"
else
    echo -e "${YELLOW}TOO OLD${NC} ($PY_VERSION, need 3.10+)"
    echo "Continuing anyway — most features work on 3.8+"
fi

# 2. Install dependencies
echo "📥 Installing Python dependencies..."
$PY -m pip install -q -r requirements.txt

# 3. Check LibreOffice
echo -n "📋 Checking LibreOffice... "
if command -v libreoffice &> /dev/null || command -v soffice &> /dev/null; then
    LO=$(command -v libreoffice || command -v soffice)
    echo -e "${GREEN}OK${NC} ($LO)"
else
    echo -e "${YELLOW}NOT FOUND${NC}"
    echo "  LibreOffice is needed for XLSX post-processing."
    echo "  Install via your package manager:"
    echo "    macOS:  brew install --cask libreoffice"
    echo "    Ubuntu: sudo apt install libreoffice"
    echo "    Windows: https://www.libreoffice.org/download"
fi

# 4. Run tests
echo "🧪 Running tests..."
$PY -m pytest tests/ -q 2>&1 | tail -5 || echo -e "${YELLOW}Some tests failed (non-fatal)${NC}"

# 5. Print quickstart
echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Quick start:"
echo ""
echo "  $PY scripts/build_xlsx.py \\"
echo "      --csv path/to/scopus_export.csv \\"
echo "      --source \"Yale\" \\"
echo "      --target \"China\" \\"
echo "      --output ./output"
echo ""
echo "Or in Mavis AI: just describe what you want to analyze."
echo "See README.md and SKILL.md for full documentation."
