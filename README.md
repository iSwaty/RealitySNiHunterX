#  Reality SNI Hunter

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

**Reality SNI Hunter** is a topology-aware scanner that helps locate Server Name Indication (SNI) domains suitable for use with V2Ray/Xray Reality. It focuses on finding domains served from IP ranges physically and numerically close to your VPS so that Reality handshake traffic blends with legitimate datacenter traffic.

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

## Why Neighbor SNI Matters?

- Topology: When an SNI is in the same /24 subnet and shares the same ASN, traffic to your VPS and to the donor site traverses the same backbone links. A censor sees traffic heading to an Amazon/DigitalOcean cluster and the packets go where packets for that SNI should go.

- Jitter & Latency: If you pick an SNI with 200 ms ping while your VPS responds in 30 ms, deep inspection systems will spot the anomaly (fake handshake timing). This scanner looks for IPs with minimal ping difference (Score).

- H2 Support: Reality mimics modern browsers which use HTTP/2. Using a site without H2 (only HTTP/1.1) is an immediate flag for blocking.

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

## Building an executable (optional)

You can package the app with PyInstaller (example):

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

The compiled binary will be available in the `dist/` folder:
- **Linux**: `dist/main` (ELF 64-bit executable)
- **Windows**: `dist/main.exe` (build on Windows)
- **macOS**: `dist/main` (build on macOS, requires `brew install python-tk@3.10` if Tkinter is missing)

> **Note:** PyInstaller creates platform-specific binaries. To get `.exe` for Windows, run the build command on a Windows machine. For macOS binary, run on a Mac. The current `dist/main` is built for Linux x86_64.

### macOS Specific

If Python is built without Tkinter support, install it via Homebrew before building:

```bash
brew install python-tk@3.10
```

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

**Reality SNI Hunter** — это сканер, ориентированный на топологию сети, который помогает находить SNI (Server Name Indication) домены, подходящие для использования с V2Ray/Xray Reality. Инструмент ищет домены в IP-диапазонах, физически и численно близких к вашему VPS, чтобы трафик выглядел естественным для дата-центра.

- Топологически-осознанное сканирование ближайших подсетей.
- Проверка поддержки HTTP/2 и TLS 1.3.
- Фильтрация служебных/тестовых имён и исключение CDN/Cloudflare.
- Экспорт результатов в JSON/TXT.

### Почему соседний SNI важен?

- Топология: Когда SNI находится в той же подсети (/24) и имеет тот же ASN, трафик до вашего VPS и до сайта-донора идет по одним и тем же магистральным кабелям. Цензор видит, что вы стучитесь в кластер серверов Amazon/DigitalOcean, и пакеты идут туда, куда и должны идти пакеты к этому SNI.

- Jitter и задержка: Если вы выберете SNI с пингом 200 мс, а ваш VPS отвечает за 30 мс, системы глубокого анализа (DPI) увидят аномалию (фейковое время рукопожатия). Этот сканер ищет IP с минимальной разницей в пинге (Score).

- Поддержка H2: Reality имитирует современные браузеры, которые используют HTTP/2. Использование сайта без H2 (только HTTP/1.1) — мгновенный флаг для блокировки.

Установка и использование те же, что описаны выше — используйте `requirements.txt` и запускайте `python main.py` или собранный бинарник. Запуск сетевых сканирований может регулироваться провайдером.

---

## 🇨🇳 简体中文

**Reality SNI Hunter** 是一款面向拓扑的扫描工具，用于查找适合 V2Ray/Xray Reality 使用的 SNI（服务器名称指示）域名。该工具优先扫描与您的 VPS 在物理或数字上接近的 IP 段，使 Reality 握手流量更像是来自同一数据中心的合法流量。

- 拓扑感知扫描：优先邻近子网。
- 协议校验：验证 HTTP/2 与 TLS 1.3 支持。
- 智能过滤：剔除测试/默认/容器化主机名，跳过 CDN/Cloudflare 代理的主机。
- 支持导出为 JSON / TXT。

### 为什么邻近 SNI 很重要？

- 拓扑：当 SNI 位于相同的 /24 子网并且属于相同的 ASN 时，指向您 VPS 与指向目标站点的流量会走相同的骨干链路。审查方会看到流量指向像 Amazon/DigitalOcean 这样的服务器集群，数据包会按该 SNI 应去的路径传输。

- 抖动与延迟：如果您选择的 SNI 延迟为 200 ms，而您的 VPS 延迟为 30 ms，深度检测系统（DPI）会发现异常（伪造的握手时序）。该扫描器寻找延迟差异最小的 IP（Score）。

- H2 支持：Reality 模拟使用 HTTP/2 的现代浏览器。使用仅支持 HTTP/1.1 的站点会成为被封锁的明显标志。

安装与使用请参照上文说明：使用 `requirements.txt` 安装依赖，并通过 `python main.py` 或打包后的可执行文件运行。进行网络扫描时请遵守服务提供商的使用条款。
