# GeneEssenceGUI

Machine Learning model training, prediction, and ensemble analysis desktop application with an intuitive graphical interface.

## Requirements

- **Python**: 3.12 or higher
- **Java**: Required for the dataset preparation step (`java` must be on PATH)
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: See `requirements.txt`

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd GeneEssenceGUI
```

### 2. Create Virtual Environment

```bash
python3.12 -m venv .venv
```

Activate the virtual environment:

- **Windows**:
  ```batch
  .venv\Scripts\activate
  ```

- **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Locally

```bash
python GeneEssenceGUI.py
```

### With Docker

**macOS (XQuartz required for GUI):**

```bash
docker run --rm \
  -e DISPLAY=host.docker.internal:0 \
  -e HOST_HOME=$HOME \
  -v /Users:/Users \
  -v /path/to/your/Dataset:/data \
  geneessencegui:v1.0.0
```

> Replace `/path/to/your/Dataset` with the absolute path to your dataset directory (e.g. `$HOME/Downloads/Dataset`).

**Build the image first (if not already built):**

```bash
docker build -t geneessencegui:v1.0.0 .
```

## Project Structure

```
GeneEssenceGUI/
├── GeneEssenceGUI.py              # Main application entry point
├── prepareDataset2RNA.jar         # Dataset preparation tool (requires Java)
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Docker Compose configuration
├── .env.example                   # Email credentials template
├── assets/                        # Images and icons
├── gene_essence_engine/           # ML processing layer (runs in subprocess)
│   ├── engine_launcher.py
│   ├── engine_worker.py
│   ├── engine_software.py
│   ├── analyse_type/              # Training, prediction, ensemble pipelines
│   ├── train_classifiers/
│   ├── evaluate_model/
│   ├── normalize_data/
│   ├── graphics/
│   └── utils/
└── gene_essence_interface/        # GUI layer (Tkinter)
    ├── pages/
    │   ├── PageManager.py         # Router and shared state
    │   ├── PrepareDataset/        # Dataset preparation wizard
    │   ├── StartPage/
    │   ├── ChooseAnalysisType/
    │   ├── InformationProject/
    │   ├── ChooseModels/
    │   ├── ChooseMetrics/
    │   ├── ChooseHowToReceiveTheResults/
    │   ├── ConfirmInformationFrame/
    │   ├── RunAnalysis/
    │   └── components/            # Reusable UI widgets
    ├── database/                  # SQLite setup, queries and fixtures
    ├── config/                    # Colors and constants
    └── utils/                     # Path resolution, DB connection
```

## Database

The application uses SQLite to store project information:
- **Location**: `gene_essence_gui.db` (created automatically next to the executable)
- **Tables**: `project` (run history), `models` (classifiers with hyperparameters), `metrics`

## Environment Setup (Email Delivery)

Copy `.env.example` to `.env` and fill in Gmail credentials:

```
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password   # Gmail App Password, not account password
```

## Troubleshooting

### Dataset Preparation Fails

- Ensure Java is installed and accessible: `java -version`
- Verify input files exist and paths contain no special characters
- Check the terminal log for the specific error from the JAR

### Application Won't Start

1. Verify Python version: `python --version` (should be 3.12+)
2. Check all dependencies installed: `pip install -r requirements.txt`
3. Ensure virtual environment is activated

### Platform-Specific Issues

- **Linux**: If directory opening fails, ensure `xdg-open` is installed
- **Windows**: Run as administrator if permission errors occur