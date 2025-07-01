# Crawly 🕷️

**Professional Playwright Script Manager** - Een krachtige GUI-applicatie voor het beheren en uitvoeren van Playwright web automation scripts.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Playwright](https://img.shields.io/badge/playwright-v1.40+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

- 🎯 **Intuitive GUI** - Gebruiksvriendelijke interface voor script management
- 🎬 **Script Recording** - Neem automatisch nieuwe scripts op met Playwright codegen
- 🔄 **Live Output** - Real-time script uitvoer en logging
- 🏗️ **Auto Setup** - Automatische virtual environment en dependency management
- 🎨 **Professional UI** - Native look-and-feel voor macOS en Windows
- 📁 **Script Library** - Organiseer en beheer al je automation scripts

## 🚀 Quick Start

### 1. Clone de Repository
```bash
git clone https://github.com/Swanta8/Crawly.git
cd Crawly
```

### 2. Automatische Setup & Start
```bash
# Één commando voor complete setup en start
python run.py
```

**Of handmatige setup:**
```bash
# Setup virtual environment en dependencies
python setup.py

# Start de applicatie
python main.py
```

### 3. Klaar! 🎉
De applicatie opent automatisch met een professionele GUI interface.

## 💻 Terminal Usage

### Direct Script Uitvoeren
```bash
# Voer een specifiek script uit
python -m playwright codegen https://example.com

# Of gebruik de virtual environment
./venv/bin/python scripts/your_script.py  # macOS/Linux
venv\Scripts\python scripts\your_script.py  # Windows
```

### API/CLI Usage
```bash
# Start de GUI applicatie
curl -X POST "file://$(pwd)/run.py" || python run.py

# Voor programmers: gebruik Python directly
python -c "
import subprocess
import sys
from pathlib import Path

# Start Crawly
subprocess.run([sys.executable, 'main.py'])
"
```

## 📖 Gebruikshandleiding

### GUI Interface
1. **Script Selecteren**: Kies een script uit de dropdown
2. **Script Starten**: Klik op "Start Script"
3. **Live Monitoring**: Bekijk real-time output in het log venster
4. **Nieuwe Scripts**: Gebruik "🔴 Neem nieuw script op" voor opname

### Script Recording
1. Klik op **"🔴 Neem nieuw script op"**
2. Voer script naam en start URL in
3. Crawly opent automatisch een browser
4. Voer je acties uit in de browser
5. Het script wordt automatisch opgeslagen

### Voorbeeld Scripts
De applicatie komt met voorbeelden:
- `configurator.py` - Formulier automatisering
- `Offerte aanvraag.py` - E-commerce workflow

## 🛠️ Requirements

- **Python 3.8+**
- **Playwright 1.40+**
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

### Dependencies (automatisch geïnstalleerd)
```txt
playwright>=1.40.0
rich>=13.0.0
pyinstaller>=6.0.0
```

## 📁 Project Structuur

```
Crawly/
├── main.py              # Hoofd GUI applicatie
├── run.py               # Quick start script
├── setup.py             # Automatische setup
├── requirements.txt     # Python dependencies
├── scripts/             # Playwright scripts
│   ├── configurator.py
│   └── Offerte aanvraag.py
├── logs/                # Script logs
└── venv/                # Virtual environment (auto-created)
```

## 🔧 Advanced Usage

### Custom Scripts Toevoegen
1. Plaats `.py` files in de `scripts/` folder
2. Gebruik standaard Playwright syntax:
```python
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    # Your automation code here
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
```

### Build Standalone App
```bash
python build.py  # Creëert executable
```

## 🚨 Troubleshooting

### Common Issues
```bash
# Permission errors (macOS/Linux)
chmod +x run.py

# Python not found
python3 run.py  # Try python3 instead of python

# Missing dependencies
python setup.py  # Re-run setup

# Browser issues
python -m playwright install  # Reinstall browsers
```

### Logs
Check `logs/` directory voor gedetailleerde error logs.

## 🤝 Contributing

1. Fork het project
2. Maak een feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit je changes (`git commit -m 'Add AmazingFeature'`)
4. Push naar de branch (`git push origin feature/AmazingFeature`)
5. Open een Pull Request

## 📝 License

Dit project is open source en beschikbaar onder de [MIT License](LICENSE).

## 🙋‍♂️ Support

- 📧 **Issues**: [GitHub Issues](https://github.com/Swanta8/Crawly/issues)
- 📖 **Documentation**: [Playwright Docs](https://playwright.dev/python/)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Swanta8/Crawly/discussions)

---

**Gemaakt met ❤️ voor web automation** 🚀

