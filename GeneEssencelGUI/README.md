# GeneEssenceGUI

Machine Learning model training, prediction, and ensemble analysis desktop application with an intuitive graphical interface.

## Overview

GeneEssenceGUI is a desktop application that simplifies machine learning workflows by providing a user-friendly interface for:
- Preparing RNA/genomic datasets from raw biological files
- Training multiple ML models simultaneously
- Making predictions with pre-trained models
- Creating ensemble models by combining multiple classifiers
- Evaluating models with various performance metrics
- Exporting results via email or local storage

## Features

- **Dataset Preparation**
  - Converts raw biological files (FASTA, GenBank, annotation CSV) into ML-ready datasets
  - Supports training and prediction dataset modes
  - Powered by `prepareDataset2RNA.jar` (requires Java)

- **Multiple Analysis Types**
  - **Training**: Train models from scratch using your dataset
  - **Prediction**: Use pre-trained models to make predictions
  - **Ensemble**: Combine multiple models for improved accuracy

- **Supported Models**
  - Decision Tree Classifier
  - Random Forest Classifier
  - Support Vector Classifier (SVC)
  - K-Nearest Neighbors (KNN)
  - Logistic Regression
  - Gradient Boosting Classifier
  - AdaBoost Classifier
  - Multi-Layer Perceptron (MLP)

- **Evaluation Metrics**
  - Accuracy
  - Precision
  - Recall
  - F1 Score
  - ROC AUC
  - Confusion Matrix

- **Flexible Result Delivery**
  - Email delivery with ZIP attachment
  - Local folder storage
  - Comprehensive reports with visualizations

## Requirements

- **Python**: 3.12 or higher
- **Java**: Required for the dataset preparation step (`java` must be on PATH)
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: See `requirements.txt`

## Docker

The only requirement is **Docker** and an **X11 server** on the host. No Python, Java, or any other dependency needed.

| Platform | X11 server |
|----------|-----------|
| Linux | Built-in (works out of the box) |
| macOS | [XQuartz](https://www.xquartz.org/) |
| Windows | [VcXsrv](https://sourceforge.net/projects/vcxsrv/) or [Xming](https://sourceforge.net/projects/xming/) |

### Quick start

```bash
# 1. Clone the repository
git clone <repository-url>
cd GeneEssenceGUI

# 2. (macOS/Windows) Allow X11 connections from Docker
xhost +local:docker

# 3. Start the application
docker compose up --build
```

The first build takes a few minutes while Docker downloads dependencies. Subsequent starts are fast.

### Using your own dataset files

Because the app runs inside a container, the file browser only sees files that are inside it. Mount the folder where your CSV/FASTA/GenBank files are:

```bash
docker compose run --rm \
  -v /path/to/your/data:/data \
  geneessence
```

Your files will then be available under `/data` inside the app's file browser.

### Email delivery (optional)

Only needed if you want to send results by email. Create a `.env` file from the example before starting:

```bash
cp .env.example .env
# open .env and fill in your Gmail credentials
docker compose up --build
```

### Data persistence

The SQLite database (project history) is stored in a Docker named volume and survives container restarts. To reset it:

```bash
docker compose down -v
```

---

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

```bash
python GeneEssenceGUI.py
```

## Building Executables

PyInstaller is already included in `requirements.txt`. Run the script for your platform from the project root:

```bash
# macOS
./build_macos.sh

# Linux
./build_linux.sh

# Windows
build_windows.bat
```

The output is placed in `dist/`:
- **macOS**: `dist/GeneEssenceGUI.app`
- **Linux / Windows**: `dist/GeneEssenceGUI/GeneEssenceGUI`

> **Linux**: the target machine must have `python3-tk` installed (`sudo apt install python3-tk`). The binary is tied to the glibc version of the build machine — build on the oldest distro version you want to support.
>
> **macOS**: the `.app` bundle runs on the same architecture as the build machine (arm64 or x86_64). Universal binaries require separate builds on each architecture.

## Usage

### Workflow A — Prepare Dataset then Analyze

Use this workflow when starting from raw biological files.

#### 1. Prepare Dataset

From the Start Page, choose **Prepare Dataset**. Select the preparation mode:

- **Training**: Provide an annotation CSV, a FASTA file, and a GenBank directory. The JAR generates a training-ready CSV.
- **Prediction**: Provide a GenBank directory. The JAR generates a prediction-ready CSV.

The terminal log shows real-time output from the preparation process. On success, the output path is shown in the banner.

#### 2. Proceed to Analysis

After preparation, continue to the ML analysis workflow below.

---

### Workflow B — Analyze an Existing Dataset

Use this workflow when you already have a CSV dataset.

#### 1. Choose Analysis Type

Select one of three analysis types:
- **Training**: Train new models from your dataset
- **Prediction**: Use existing models to make predictions
- **Ensemble**: Combine multiple models

#### 2. Configure Project

- **Project Name**: Enter a unique name (5–10 characters)
- **CSV File**: Select your dataset file
- **Test Size**: Choose train/test split ratio (default: 0.3)

#### 3. Select Models

Choose one or more machine learning models to train or use.

#### 4. Select Metrics

Choose evaluation metrics to assess model performance.

#### 5. Choose Delivery Method

- **Email**: Receive results as a ZIP file via email
- **Local**: Save results to a folder on your computer

#### 6. Run Analysis

Click "Run Analysis" and monitor real-time progress in the terminal log. Results will be delivered according to your chosen method.

## CSV File Format

Your input CSV file must follow this format:

- **Columns**: Feature columns followed by target column
- **Last Column**: Must be the target variable (class labels)
- **Encoding**: UTF-8
- **No Missing Values**: All cells must have values

### Example CSV

```csv
Feature1,Feature2,Feature3,Target
1.0,2.0,3.0,ClassA
1.5,2.5,3.5,ClassB
2.0,3.0,4.0,ClassA
2.5,3.5,4.5,ClassC
```

## Project Structure

```
GeneEssenceGUI/
├── GeneEssenceGUI.py              # Main application entry point
├── prepareDataset2RNA.jar         # Dataset preparation tool (requires Java)
├── requirements.txt               # Python dependencies
├── build_macos.sh                 # PyInstaller build script for macOS
├── build_linux.sh                 # PyInstaller build script for Linux
├── build_windows.bat              # PyInstaller build script for Windows
├── Dockerfile                     # Docker image definition
├── docker-compose.yml             # Docker Compose configuration
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
    ├── database/                  # SQLite setup and queries
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

### CSV File Errors

- Ensure file is UTF-8 encoded
- Check that all columns have headers
- Verify no missing values exist
- Confirm last column is the target variable

### Application Won't Start

1. Verify Python version: `python --version` (should be 3.12+)
2. Check all dependencies installed: `pip install -r requirements.txt`
3. Ensure virtual environment is activated

### Platform-Specific Issues

- **Linux**: If directory opening fails, ensure `xdg-open` is installed
- **Windows**: Run as administrator if permission errors occur