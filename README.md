# Reality SNI Hunter v7.1

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey) ![Version](https://img.shields.io/badge/Version-7.1-red)

**Reality SNI Hunter** is a topology-aware scanner that helps locate Server Name Indication (SNI) domains suitable for use with V2Ray/Xray Reality. It focuses on finding domains served from IP ranges physically and numerically close to your VPS so that Reality handshake traffic blends with legitimate datacenter traffic.

## 🚀 What's New in v7.1

- **Enhanced Domain Filtering:** Comprehensive blacklist including VK Portal, Yandex all countries (with Punycode support for Cyrillic domains like яндекс.рф), all *.yimg.com subdomains, IGN network
- **VPN Keyword Filter:** Automatically blocks any domain containing "vpn" keyword
- **Invalid Domain Filter:** Blocks .invalid TLD and malformed domains like "invalid2.invalid"
- **Improved Subdomain Detection:** Advanced pattern matching for vkvideo.ru, vk-portal.ru, stats.vk-portal.net, m.vkvideo.ru
- **Performance Optimization:** Using frozenset for O(1) lookup time in blacklist checks
- **Better Cyrillic Support:** Automatic IDNA/Punycode conversion for кириллические домены

## Overview

- **Topology-aware scanning:** Prioritizes nearby subnets to increase the chance that the SNI is served from the same rack/switch.
- **Protocol checks:** Verifies HTTP/2 and TLS 1.3 support required by Reality.
- **Filtering & heuristics:** Removes test/k8s/traefik hostnames, expands wildcards, and skips Cloudflare/CDN-proxied hosts.
- **Exportable results:** Save findings as JSON or TXT for later use.

## Features

- Neighbor scanning (adjacent subnets)
- Distance scoring (latency + numerical distance)
- ASN highlighting (same Autonomous System)
- H2 and TLS 1.3 verification
- Smart domain filtering and wildcard expansion
- GUI with dark theme, sortable columns, export options
- Multi-language support (Russian, English, Chinese)

## Why Neighbor SNI Matters?

- **Topology:** When an SNI is in the same /24 subnet and shares the same ASN, traffic to your VPS and to the donor site traverses the same backbone links. A censor sees traffic heading to an Amazon/DigitalOcean cluster and the packets go where packets for that SNI should go.

- **Jitter & Latency:** If you pick an SNI with 200 ms ping while your VPS responds in 30 ms, deep inspection systems will spot the anomaly (fake handshake timing). This scanner looks for IPs with minimal ping difference (Score).

- **H2 Support:** Reality mimics modern browsers which use HTTP/2. Using a site without H2 (only HTTP/1.1) is an immediate flag for blocking.

## Requirements

- Python 3.10 or newer
- See `requirements.txt` for Python dependencies

## Installation

1. Clone or download this repository.
2. (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows (PowerShell)
source .venv/bin/activate      # Linux / macOS
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### macOS Specific

If Python is built without Tkinter support, install it via Homebrew:

```bash
brew install python-tk@3.10
```

## Usage

- Quick run (show help and options):

```bash
python main.py --help
```

- Typical workflow:
    - Run `python main.py` (or the platform binary) on your VPS.
    - Allow the scanner to probe nearby subnets and collect candidate hostnames.
    - Review results in the GUI or exported JSON/TXT files.

Notes:
- Exact CLI flags and configuration options depend on `main.py`. Use `--help` to list available switches.
- Running active network scans may be restricted by your provider—use responsibly and within terms of service.

## Building Executables

### Windows (.exe)

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. Open Command Prompt or PowerShell as Administrator
3. Navigate to project directory:
   ```cmd
   cd path\to\RealitySNiHunterX
   ```
4. Create virtual environment and activate:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
5. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```
6. Build executable:
   ```cmd
   pyinstaller --onefile --windowed --name "Reality_SNI_Hunter_v7" --icon=NONE main.py
   ```
7. Find your `.exe` in `dist\Reality_SNI_Hunter_v7.exe`

**PyInstaller Options Explained:**
- `--onefile`: Single executable file
- `--windowed`: No console window (GUI app)
- `--name`: Custom name for executable
- `--icon`: Custom icon file (optional, use `.ico` format)

### macOS (.app / binary)

1. Install Homebrew if not installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python with Tkinter support:
   ```bash
   brew install python-tk@3.10
   ```
3. Navigate to project directory:
   ```bash
   cd /path/to/RealitySNiHunterX
   ```
4. Create virtual environment and activate:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```
6. Build executable:
   ```bash
   pyinstaller --onefile --windowed --name "Reality_SNI_Hunter_v7" --icon=NONE main.py
   ```
7. Find your binary in `dist/Reality_SNI_Hunter_v7`

**Optional: Create .app Bundle**
```bash
pyinstaller --windowed --name "Reality_SNI_Hunter_v7" main.py
```
This creates `dist/Reality_SNI_Hunter_v7.app` which can be dragged to Applications folder.

### Linux (binary)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --name "Reality_SNI_Hunter_v7" main.py
```
Binary will be in `dist/Reality_SNI_Hunter_v7`

## Development

- Code is placed in `main.py` (single-file entry). Add modules as needed for larger refactors.
- Follow standard Python packaging and testing practices when contributing.

## Contributing

Contributions are welcome. Open an issue first to discuss larger changes. For small fixes, submit a PR with a clear description and tests where appropriate.

## License

This project is released under the MIT License. See LICENSE for details.

## Acknowledgements

Inspired by community tools for privacy-preserving tunneling and Reality protocol experimentation.

## Contact

If you have questions or need help, open an issue or contact the repository maintainer.

---

## 🇷🇺 Русский

**Reality SNI Hunter v7.1** — это сканер, ориентированный на топологию сети, который помогает находить SNI (Server Name Indication) домены, подходящие для использования с V2Ray/Xray Reality. Инструмент ищет домены в IP-диапазонах, физически и численно близких к вашему VPS, чтобы трафик выглядел естественным для дата-центра.

### 🚀 Новое в версии 7.1

- **Улучшенная фильтрация доменов:** Расширенный чёрный список включая VK Portal, Яндекс все страны (с поддержкой Punycode для кириллических доменов типа яндекс.рф), все поддомены *.yimg.com, сеть IGN
- **Фильтр по ключевому слову VPN:** Автоматически блокирует любые домены содержащие "vpn"
- **Фильтр некорректных доменов:** Блокирует .invalid TLD и malformed домены типа "invalid2.invalid"
- **Улучшенное обнаружение поддоменов:** Продвинутое сопоставление шаблонов для vkvideo.ru, vk-portal.ru, stats.vk-portal.net, m.vkvideo.ru
- **Оптимизация производительности:** Использование frozenset для O(1) времени поиска в чёрном списке
- **Улучшенная поддержка кириллицы:** Автоматическая конвертация IDNA/Punycode для кириллических доменов

### Возможности

- Топологически-осознанное сканирование ближайших подсетей.
- Проверка поддержки HTTP/2 и TLS 1.3.
- Фильтрация служебных/тестовых имён и исключение CDN/Cloudflare.
- Экспорт результатов в JSON/TXT.
- Многоязычный интерфейс (русский, английский, китайский).

### Почему соседний SNI важен?

- **Топология:** Когда SNI находится в той же подсети (/24) и имеет тот же ASN, трафик до вашего VPS и до сайта-донора идет по одним и тем же магистральным кабелям. Цензор видит, что вы стучитесь в кластер серверов Amazon/DigitalOcean, и пакеты идут туда, куда и должны идти пакеты к этому SNI.

- **Jitter и задержка:** Если вы выберете SNI с пингом 200 мс, а ваш VPS отвечает за 30 мс, системы глубокого анализа (DPI) увидят аномалию (фейковое время рукопожатия). Этот сканер ищет IP с минимальной разницей в пинге (Score).

- **Поддержка H2:** Reality имитирует современные браузеры, которые используют HTTP/2. Использование сайта без H2 (только HTTP/1.1) — мгновенный флаг для блокировки.

### Установка

1. Клонируйте репозиторий или скачайте архив.
2. Создайте виртуальное окружение (рекомендуется):
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   source .venv/bin/activate      # Linux/macOS
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

#### macOS

Если Python собран без поддержки Tkinter:
```bash
brew install python-tk@3.10
```

### Запуск

```bash
python main.py
```

### Сборка исполняемых файлов

#### Windows (.exe)

1. Установите Python 3.10+ с [python.org](https://www.python.org/downloads/)
2. Откройте Command Prompt или PowerShell от имени администратора
3. Перейдите в директорию проекта:
   ```cmd
   cd путь\к\RealitySNiHunterX
   ```
4. Создайте и активируйте виртуальное окружение:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
5. Установите зависимости:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```
6. Соберите exe-файл:
   ```cmd
   pyinstaller --onefile --windowed --name "Reality_SNI_Hunter_v7" main.py
   ```
7. Готовый файл: `dist\Reality_SNI_Hunter_v7.exe`

#### macOS

1. Установите Homebrew (если не установлен):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Установите Python с поддержкой Tkinter:
   ```bash
   brew install python-tk@3.10
   ```
3. Установите зависимости и соберите:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install pyinstaller
   pyinstaller --onefile --windowed --name "Reality_SNI_Hunter_v7" main.py
   ```
4. Бинарник: `dist/Reality_SNI_Hunter_v7`

#### Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --name "Reality_SNI_Hunter_v7" main.py
```

---

## 🇨🇳 简体中文

**Reality SNI Hunter v7.1** 是一款面向拓扑的扫描工具，用于查找适合 V2Ray/Xray Reality 使用的 SNI（服务器名称指示）域名。该工具优先扫描与您的 VPS 在物理或数字上接近的 IP 段，使 Reality 握手流量更像是来自同一数据中心的合法流量。

### 🚀 7.1 版本新功能

- **增强域名过滤：** 全面黑名单包括 VK Portal、Yandex 所有国家（支持 Punycode 转换西里尔域名如 яндекс.рф）、所有 *.yimg.com 子域名、IGN 网络
- **VPN 关键词过滤：** 自动拦截任何包含 "vpn" 关键词的域名
- **无效域名过滤：** 拦截 .invalid TLD 和格式错误的域名如 "invalid2.invalid"
- **改进的子域名检测：** 高级模式匹配 vkvideo.ru、vk-portal.ru、stats.vk-portal.net、m.vkvideo.ru
- **性能优化：** 使用 frozenset 实现 O(1) 查找时间的黑名单检查
- **更好的西里尔文支持：** 自动 IDNA/Punycode 转换 кириллические домены

### 功能特性

- 拓扑感知扫描：优先邻近子网。
- 协议校验：验证 HTTP/2 与 TLS 1.3 支持。
- 智能过滤：剔除测试/默认/容器化主机名，跳过 CDN/Cloudflare 代理的主机。
- 支持导出为 JSON / TXT。
- 多语言界面（俄语、英语、中文）。

### 为什么邻近 SNI 很重要？

- **拓扑：** 当 SNI 位于相同的 /24 子网并且属于相同的 ASN 时，指向您 VPS 与指向目标站点的流量会走相同的骨干链路。审查方会看到流量指向像 Amazon/DigitalOcean 这样的服务器集群，数据包会按该 SNI 应去的路径传输。

- **抖动与延迟：** 如果您选择的 SNI 延迟为 200 ms，而您的 VPS 延迟为 30 ms，深度检测系统（DPI）会发现异常（伪造的握手时序）。该扫描器寻找延迟差异最小的 IP（Score）。

- **H2 支持：** Reality 模拟使用 HTTP/2 的现代浏览器。使用仅支持 HTTP/1.1 的站点会成为被封锁的明显标志。

### 安装

1. 克隆或下载此仓库。
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   source .venv/bin/activate      # Linux/macOS
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

#### macOS 特别说明

如果 Python 没有 Tkinter 支持：
```bash
brew install python-tk@3.10
```

### 运行

```bash
python main.py
```

### 构建可执行文件

#### Windows (.exe)

1. 从 [python.org](https://www.python.org/downloads/) 安装 Python 3.10+
2. 以管理员身份打开命令提示符或 PowerShell
3. 进入项目目录：
   ```cmd
   cd 路径\到\RealitySNiHunterX
   ```
4. 创建并激活虚拟环境：
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
5. 安装依赖：
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```
6. 构建可执行文件：
   ```cmd
   pyinstaller --onefile --windowed --name "Reality_SNI_Hunter_v7" main.py
   ```
7. 生成的文件：`dist\Reality_SNI_Hunter_v7.exe`

#### macOS

1. 安装 Homebrew（如未安装）：
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. 安装带 Tkinter 支持的 Python：
   ```bash
   brew install python-tk@3.10
   ```
3. 安装依赖并构建：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install pyinstaller
   pyinstaller --onefile --windowed --name "Reality_SNI_Hunter_v7" main.py
   ```
4. 生成的二进制文件：`dist/Reality_SNI_Hunter_v7`

#### Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --name "Reality_SNI_Hunter_v7" main.py
```

---

**Happy Scanning! / Удачного сканирования! / 扫描愉快！**
