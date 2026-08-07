# CodeRun Stats

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CodeRun](https://img.shields.io/badge/Source-CodeRun-yellow.svg)](https://coderun.yandex.ru/)
[![GitHub Actions](https://img.shields.io/badge/Automation-GitHub%20Actions-2088FF.svg)](https://github.com/features/actions)

Automatically generate a beautiful SVG card with your CodeRun statistics (solved problems by difficulty, competition standings) and embed it into your README. Perfect for showcasing your coding progress on GitHub.

## What people see
<!-- CODE_RUN_STATS_START -->
<!-- CODE_RUN_STATS_END -->

## Features

- 📊 **Solved problems** — total count with a circular progress indicator
- 🟢🟡🔴 **Difficulty breakdown** — Easy, Medium, Hard with progress bars
- 🏆 **Competition info** — current season standings (place, score, solved)
- 🔄 **Auto-update** — runs every 6 hours via GitHub Actions (or manually on demand)
- 🎨 **GitHub-themed** — fits perfectly into your profile README

## Installation Local

### Prerequisites

- Python 3.8 or higher
- `pip` and `git`

### Steps

1. **Fork/clone the repository**

   ```bash
   git clone https://github.com/your-username/coderun-stats.git
   cd coderun-stats
   ```

2. **Set up local environment variables** (for manual runs)

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your CodeRun data:

   ```env
   PROFILE=your_coderun_username
   BASE_URL=https://coderun.yandex.ru/api
   SEASON=2026-summer    # e.g. 2026-summer, 2025-winter, etc.
   # optional:
   # SVG_OUTPUT=stats.svg
   # README_PATH=README.md
   # TIMEOUT=10
   ```

3. **Install the package in development mode**

   ```bash
   pip install -e .
   ```

   (This installs all dependencies defined in `pyproject.toml`.)

## Usage

### Manual run (local)

```bash
python -m src.main
```

or, if you installed the package with a console script:

```bash
coderun-stats
```

The script will:

1. fetch your stats from the CodeRun API,
2. generate `stats.svg`,
3. replace the content between `<!-- CODE_RUN_STATS_START -->` and `<!-- CODE_RUN_STATS_END -->` in your `README.md`.

### Automated via GitHub Actions

The included workflow (`.github/workflows/update-stats.yml`) runs:

- every 6 hours,
- on `workflow_dispatch` (manual trigger from the Actions tab),
- on pushes to `README.md`.

To use it, you must configure GitHub Secrets with your CodeRun credentials.
Go to your repository **Settings → Secrets and variables → Actions**, and add the following secrets:

| Secret name | Example value                    |
|-------------|-----------------------------------|
| `PROFILE`   | `Name_Code_Run`                        |
| `BASE_URL`  | `https://coderun.yandex.ru/api`   |
| `SEASON`    | `2026-summer`                     |

**Why secrets?**
This keeps your username and season settings private and makes the workflow reusable for different users without hard-coding values.

No `.env` file is needed in the GitHub runner — the workflow passes these secrets as environment variables directly.

## Project Structure

```
coderun-stats/
├── src/                         # Main package
│   ├── __init__.py
│   ├── main.py                  # Entry point
│   ├── models.py                # Data classes (ProfileStats, CompetitionInfo)
│   ├── fetcher.py               # API client (requests)
│   ├── renderer.py              # SVG generator
│   └── updater.py               # Saves SVG and updates README
├── .github/
│   └── workflows/
│       └── update-stats.yml     # GitHub Actions workflow
├── pyproject.toml               # Project metadata & dependencies
├── .env.example                 # Template for environment variables
├── .gitignore
└── README.md                    # This file
```

## Configuration

All settings are read from environment variables:

| Variable      | Description                     | Required | Default     |
|----------------|----------------------------------|----------|-------------|
| `PROFILE`      | Your CodeRun username           | Yes      | —           |
| `BASE_URL`     | API base URL                    | Yes      | —           |
| `SEASON`       | Season name (e.g. `2026-summer`)| Yes      | —           |
| `SVG_OUTPUT`   | Output SVG filename             | No       | `stats.svg` |
| `README_PATH`  | Path to README file             | No       | `README.md` |
| `TIMEOUT`      | HTTP request timeout (seconds)  | No       | `10`        |

> **Note:** If the user has not participated in any competition for the given season, the script will gracefully display a "No active competitions" message.

## Customisation

To change colours or dimensions, edit the `colors` dictionary in `main.py` (or pass a custom dict via `config["colors"]`). The SVG uses GitHub's dark theme (`#0d1117`, `#e6edf3`, etc.).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
