# Reality SNI Hunter v5.3 (Clean Core)

[🇷🇺 Русский](#-русский) | [🇬🇧 English](#-english) | [🇨🇳 简体中文](#-简体中文)

---

## 🇷🇺 Русский

### Описание
Reality SNI Hunter — это инструмент для поиска подходящих SNI доменов для обхода блокировок Reality. Программа сканирует соседние IP-адреса или широкие диапазоны ASN, находя "чистые" домены, которые не фильтруются известными сервисами.

### Особенности
- ✅ **Расширенная фильтрация**: Исключает более 150 известных доменов (Google, Yandex, VK, Wikipedia, Netflix и др.)
- ✅ **Два режима сканирования**: 
  - Соседние подсети (±5 от IP VPS)
  - Широкий поиск по ASN (/16 сеть)
- ✅ **Фильтрация по стране**: Можно искать только домены из страны вашего VPS
- ✅ **Рейтинг доменов**: Оценка качества найденных SNI
- ✅ **Экспорт результатов**: JSON, TXT, копирование в буфер
- ✅ **Сортировка**: По домену, IP, ASN, рейтингу
- ✅ **Мультиязычность**: Русский, English, 简体中文

### Установка

#### Требования
- Python 3.8–3.12
- Библиотеки: `customtkinter`, `maxminddb`, `pyOpenSSL`, `cryptography`, `pyperclip`

#### Шаг 1: Установка зависимостей
```bash
pip install -r requirements.txt
```

#### Шаг 2: Базы данных GeoIP
Скачайте базы данных MaxMind (бесплатно):
- [Country.mmdb](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
- [ASN.mmdb](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)

Поместите файлы в папку с программой.

#### Для macOS (если Python без Tkinter)
Если при запуске ошибка о отсутствии Tkinter:
```bash
brew install python-tk@3.10
# или для вашей версии Python
brew install python-tk@3.11
brew install python-tk@3.12
```

### Запуск
```bash
python main.py
```

### Сборка исполняемых файлов

#### Linux
```bash
pip install pyinstaller
pyinstaller --onefile main.py
# Бинарник: dist/main
```

#### Windows (.exe)
Запустите на Windows:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Бинарник: dist/main.exe
```

#### macOS (.app / бинарник)
Запустите на macOS:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Бинарник: dist/main
```

> ⚠️ **Важно**: PyInstaller создаёт бинарники только для текущей ОС. Для кросс-платформенной сборки используйте:
> - **GitHub Actions** с матрицей ОС
> - **Docker** для эмуляции других платформ
> - **Виртуальные машины**

### Альтернативные инструменты сборки

| Инструмент | Платформы | Преимущества |
|------------|-----------|--------------|
| **PyInstaller** | Win/Mac/Linux | Самый популярный, простая настройка |
| **cx_Freeze** | Win/Mac/Linux | Хорошая поддержка Mac |
| **Nuitka** | Win/Mac/Linux | Компиляция в C++, выше производительность |
| **py2exe** | Windows | Только Windows, лёгкий |
| **py2app** | macOS | Только macOS, нативная интеграция |
| **Briefcase** | Win/Mac/Linux | Часть BeeWare, создание полноценных приложений |

#### Пример сборки через Nuitka:
```bash
pip install nuitka
python -m nuitka --onefile --windows-disable-console main.py
```

### Использование
1. Введите IP вашего VPS
2. Выберите режим сканирования
3. Установите лимит найденных доменов (или "Все")
4. Нажмите "НАЧАТЬ ПОИСК"
5. Результаты появятся в таблице
6. Экспортируйте через кнопки JSON/TXT/Копировать

### Фильтруемые домены (примеры)
**Международные**: google.*, youtube.*, facebook.*, twitter.*, instagram.*, amazon.*, netflix.*, apple.*, microsoft.*, wikipedia.*, github.*, steam.*, discord.*

**Российские**: yandex.*, ya.ru, mail.ru, vk.com, ok.ru, sberbank.*, tinkoff.*, wildberries.*, ozon.*, avito.*, lenta.*, ria.*, habr.*, kinopoisk.*, ivi.*, telegram.*, 2gis.*

---

## 🇬🇧 English

### Description
Reality SNI Hunter is a tool for finding suitable SNI domains to bypass Reality censorship. The program scans neighboring IP addresses or wide ASN ranges to find "clean" domains that are not filtered by known services.

### Features
- ✅ **Extended Filtering**: Excludes 150+ known domains (Google, Yandex, VK, Wikipedia, Netflix, etc.)
- ✅ **Two Scan Modes**: 
  - Neighbor Subnets (±5 from VPS IP)
  - Wide ASN Scan (/16 network)
- ✅ **Country Filter**: Search only for domains from your VPS country
- ✅ **Domain Rating**: Quality scoring for found SNI
- ✅ **Export Results**: JSON, TXT, copy to clipboard
- ✅ **Sorting**: By domain, IP, ASN, score
- ✅ **Multilingual**: Русский, English, 简体中文

### Installation

#### Requirements
- Python 3.8–3.12
- Libraries: `customtkinter`, `maxminddb`, `pyOpenSSL`, `cryptography`, `pyperclip`

#### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 2: GeoIP Databases
Download MaxMind databases (free):
- [Country.mmdb](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
- [ASN.mmdb](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)

Place files in the program folder.

#### For macOS (if Python without Tkinter)
If you get a Tkinter error on startup:
```bash
brew install python-tk@3.10
# or for your Python version
brew install python-tk@3.11
brew install python-tk@3.12
```

### Running
```bash
python main.py
```

### Building Executables

#### Linux
```bash
pip install pyinstaller
pyinstaller --onefile main.py
# Binary: dist/main
```

#### Windows (.exe)
Run on Windows:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Binary: dist/main.exe
```

#### macOS (.app / binary)
Run on macOS:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Binary: dist/main
```

> ⚠️ **Important**: PyInstaller creates binaries only for the current OS. For cross-platform builds use:
> - **GitHub Actions** with OS matrix
> - **Docker** for platform emulation
> - **Virtual Machines**

### Alternative Build Tools

| Tool | Platforms | Advantages |
|------|-----------|------------|
| **PyInstaller** | Win/Mac/Linux | Most popular, easy setup |
| **cx_Freeze** | Win/Mac/Linux | Good Mac support |
| **Nuitka** | Win/Mac/Linux | C++ compilation, higher performance |
| **py2exe** | Windows | Windows only, lightweight |
| **py2app** | macOS | macOS only, native integration |
| **Briefcase** | Win/Mac/Linux | Part of BeeWare, creates full apps |

#### Example build with Nuitka:
```bash
pip install nuitka
python -m nuitka --onefile --windows-disable-console main.py
```

### Usage
1. Enter your VPS IP
2. Select scan mode
3. Set limit for found domains (or "All")
4. Click "START SCAN"
5. Results appear in the table
6. Export via JSON/TXT/Copy buttons

### Filtered Domains (examples)
**International**: google.*, youtube.*, facebook.*, twitter.*, instagram.*, amazon.*, netflix.*, apple.*, microsoft.*, wikipedia.*, github.*, steam.*, discord.*

**Russian**: yandex.*, ya.ru, mail.ru, vk.com, ok.ru, sberbank.*, tinkoff.*, wildberries.*, ozon.*, avito.*, lenta.*, ria.*, habr.*, kinopoisk.*, ivi.*, telegram.*, 2gis.*

---

## 🇨🇳 简体中文

### 描述
Reality SNI Hunter 是一个用于查找适合绕过 Reality 审查的 SNI 域名的工具。该程序扫描相邻 IP 地址或广泛的 ASN 范围，寻找不被已知服务过滤的"干净"域名。

### 功能特点
- ✅ **扩展过滤**：排除 150+ 个已知域名（Google、Yandex、VK、Wikipedia、Netflix 等）
- ✅ **两种扫描模式**：
  - 邻近子网（VPS IP ±5）
  - 广泛 ASN 扫描（/16 网络）
- ✅ **国家过滤器**：仅搜索来自您 VPS 所在国家的域名
- ✅ **域名评级**：对找到的 SNI 进行质量评分
- ✅ **导出结果**：JSON、TXT、复制到剪贴板
- ✅ **排序**：按域名、IP、ASN、评分排序
- ✅ **多语言支持**：Русский、English、简体中文

### 安装

#### 系统要求
- Python 3.8–3.12
- 库：`customtkinter`、`maxminddb`、`pyOpenSSL`、`cryptography`、`pyperclip`

#### 步骤 1：安装依赖
```bash
pip install -r requirements.txt
```

#### 步骤 2：GeoIP 数据库
下载 MaxMind 数据库（免费）：
- [Country.mmdb](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
- [ASN.mmdb](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)

将文件放在程序文件夹中。

#### macOS 用户（如果 Python 没有 Tkinter）
如果启动时出现 Tkinter 错误：
```bash
brew install python-tk@3.10
# 或者根据您的 Python 版本
brew install python-tk@3.11
brew install python-tk@3.12
```

### 运行
```bash
python main.py
```

### 构建可执行文件

#### Linux
```bash
pip install pyinstaller
pyinstaller --onefile main.py
# 二进制文件：dist/main
```

#### Windows (.exe)
在 Windows 上运行：
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# 二进制文件：dist/main.exe
```

#### macOS (.app / 二进制文件)
在 macOS 上运行：
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# 二进制文件：dist/main
```

> ⚠️ **重要提示**：PyInstaller 仅为当前操作系统创建二进制文件。要跨平台构建，请使用：
> - **GitHub Actions** 与操作系统矩阵
> - **Docker** 用于平台模拟
> - **虚拟机**

### 替代构建工具

| 工具 | 平台 | 优势 |
|------|------|------|
| **PyInstaller** | Win/Mac/Linux | 最流行，设置简单 |
| **cx_Freeze** | Win/Mac/Linux | 良好的 Mac 支持 |
| **Nuitka** | Win/Mac/Linux | C++ 编译，性能更高 |
| **py2exe** | Windows | 仅限 Windows，轻量级 |
| **py2app** | macOS | 仅限 macOS，原生集成 |
| **Briefcase** | Win/Mac/Linux | BeeWare 的一部分，创建完整应用 |

#### 使用 Nuitka 构建示例：
```bash
pip install nuitka
python -m nuitka --onefile --windows-disable-console main.py
```

### 使用方法
1. 输入您的 VPS IP 地址
2. 选择扫描模式
3. 设置找到域名的限制（或"全部"）
4. 点击"开始扫描"
5. 结果将显示在表格中
6. 通过 JSON/TXT/复制按钮导出

### 被过滤的域名（示例）
**国际**：google.*、youtube.*、facebook.*、twitter.*、instagram.*、amazon.*、netflix.*、apple.*、microsoft.*、wikipedia.*、github.*、steam.*、discord.*

**俄罗斯**：yandex.*、ya.ru、mail.ru、vk.com、ok.ru、sberbank.*、tinkoff.*、wildberries.*、ozon.*、avito.*、lenta.*、ria.*、habr.*、kinopoisk.*、ivi.*、telegram.*、2gis.*

---

## Лицензия / License / 许可证
MIT License

## Контакты / Contacts / 联系方式
GitHub Issues
