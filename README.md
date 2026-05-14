<p align="center">
  <img src="screenshots/genne_essence.png" alt="GeneEssenceGUI Logo" width="200" />
</p>

<h1 align="center">GeneEssenceGUI</h1>

<p align="center">Integrating DEG and NCBI datasets through ensemble machine learning for essential gene prediction</p>

<p align="center">
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" alt="Python 3.12+" /></a>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platform" />
  <a href="https://github.com/allanverasce/geneessencegui/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/Download-v1.0.0-brightgreen" alt="Download v1.0.0" /></a>
</p>

---

GeneEssenceGUI allows researchers to classify essential genes using machine learning without requiring programming skills. The platform handles data ingestion, model training, hyperparameter optimization, and result delivery through a unified wizard interface. All experimental metadata is logged to a local SQLite database for full reproducibility.

**Key features:**
- Nine machine learning classifiers (Logistic Regression, Random Forest, SVC, and more)
- Training, Prediction, and Ensemble analysis modes
- Integrated dataset preparation module — converts raw genomic files into the CSV format required for analysis
- Configurable hyperparameters per model
- Result delivery by email or local folder
---

## Table of Contents

- [1. Installation](#1-installation)
- [2. Dataset Format](#2-dataset-format)
- [3. Main Window](#3-main-window)
- [4. Analysis Type Selection](#4-analysis-type-selection)
- [5. Training](#5-training)
- [6. Prediction](#6-prediction)
- [7. Ensemble](#7-ensemble)
- [8. Loading Existing Projects](#8-loading-existing-projects)
- [9. Prepare Dataset](#9-prepare-dataset)

---

# 1. Installation

Three installation methods are available: downloading the pre-built executable, running via Docker, or running from source.

## 1.1. Download the executable (recommended)

Pre-built executables for Windows, Linux, and macOS are available on the [releases page](https://github.com/allanverasce/geneessencegui/releases/tag/v1.0.0). No Python or dependency installation required.

| Platform | File |
|---|---|
| **Windows** | `GeneEssenceGUI.exe` |
| **Linux** | `GeneEssenceGUI` (folder) |
| **macOS** | `GeneEssenceGUI.app` |

> **Note:** Java must be installed and available in your system PATH to use the **Prepare Dataset** feature. Download it from https://www.java.com.

## 1.2. Docker

> **Note:** Replace `<dockerhub-user>` with the actual Docker Hub username once the image is published.

### Linux
```bash
xhost +local:docker
docker run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  <dockerhub-user>/geneessencegui:v1.0.0
```

### macOS
Install [XQuartz](https://www.xquartz.org/) first, then:
```bash
xhost +localhost
docker run --rm \
  -e DISPLAY=host.docker.internal:0 \
  <dockerhub-user>/geneessencegui:v1.0.0
```

### Windows
Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) and start it with **Disable access control** checked, then:
```powershell
docker run --rm -e DISPLAY=host.docker.internal:0 <dockerhub-user>/geneessencegui:v1.0.0
```

## 1.3. From source

Requires Python 3.12+ and Java (for the Prepare Dataset feature).

```bash
git clone https://github.com/allanverasce/geneessencegui.git
cd geneessencegui/GeneEssencelGUI
python -m venv .venv
```

Activate the virtual environment:

- **Windows:** `.venv\Scripts\activate`
- **Linux/macOS:** `source .venv/bin/activate`

Then install dependencies and run:

```bash
pip install -r requirements.txt
python GeneEssenceGUI.py
```

> **Note:** The **Receive by Email** delivery option is not available when running from source. The `.env` file containing the email credentials is not distributed with the repository. Use the **Save Locally** option instead.

---

# 2. Dataset Format

<p align="justify">GeneEssenceGUI requires datasets in CSV (Comma-Separated Values) format. Each row represents one gene instance. All columns except the last are treated as features; the <strong>last column must be the classification label</strong> (essential or non-essential).</p>

<p align="center">
<img src="screenshots/2. Dataset Format.jpeg" alt="Dataset format example" width="600" height="500" />
</p>

Sample datasets are provided in the `datasets/` folder of this repository.

---

# 3. Main Window

<p align="justify">When GeneEssenceGUI starts, the main window is displayed. The left sidebar shows the tool name, a brief description, a list of the four available features, and the project partners. The right panel presents two buttons to begin:</p>

- **START ANALYSIS** — opens the analysis wizard (Training, Prediction, or Ensemble).
- **PREPARE DATASET** — opens the integrated dataset preparation module.

<p align="center">
<img src="screenshots/3. Main Window.png" alt="Main Window" width="800" height="600" />
</p>

---

# 4. Analysis Type Selection

<p align="justify">Clicking <strong>START ANALYSIS</strong> opens the type selection screen. A progress sidebar on the left tracks the current step of the wizard, updating dynamically based on the type chosen. Three analysis types are available:</p>

- **Training** — trains one or more machine learning models on a labeled dataset. The wizard includes steps for model selection, metric selection, and delivery configuration.
- **Prediction** — applies a previously trained model (`.pkl`) to new data and returns the classification of each gene. The wizard goes directly from project setup to delivery configuration.
- **Ensemble** — combines multiple pre-trained models using a hard-voting strategy. Requires a directory containing `.pkl` model files. The wizard includes a metric selection step.

<p align="center">
<img src="screenshots/4. Analysis Type Selection.png" alt="Analysis Type Selection" width="800" height="600" />
</p>

---

# 5. Training

## 5.1. Project Information

<p align="justify">After selecting <strong>Training</strong>, the Project Information screen is shown. The project name must be between 5 and 10 characters. The user selects the CSV dataset file and sets the proportion of data reserved for testing (test size), from 10% to 90%.</p>

<p align="justify">If previous Training projects exist in the database, a toggle (<strong>Create new / Load existing</strong>) appears at the top. Selecting <em>Load existing</em> shows a list of saved projects whose settings are loaded automatically.</p>

<p align="center">
<img src="screenshots/5.1. Project Information.png" alt="Project Information" width="800" height="600" />
</p>

## 5.2. Model Selection

<p align="justify">The model selection screen displays the eight available classifiers in a two-column grid. At least one model must be selected to proceed. A <strong>Select All</strong> checkbox is available at the bottom of the screen.</p>

Each model card provides two action buttons:
- **⚙** (settings) — opens the parameter configuration modal for that model. This button is only enabled after the model is selected.
- **🔗** (link) — opens the official scikit-learn documentation for that model in the browser.

<p align="center">
<img src="screenshots/5.2. Model Selection.png" alt="Model Selection" width="800" height="600" />
</p>

### Model Parameters

<p align="justify">Clicking ⚙ on a selected model opens a modal window listing all configurable hyperparameters for that model. Parameters can be modified or left at their default values.</p>

<p align="center">
<img src="screenshots/Model Parameters.png" alt="Model Parameters" width="800" height="600" />
</p>

## 5.3. Metric Selection

<p align="justify">The metric selection screen lists the available evaluation metrics in a two-column grid. At least one metric must be selected. A <strong>Select All</strong> checkbox is available. The <strong>🔗</strong> button next to each metric opens its official documentation.</p>

<p align="center">
<img src="screenshots/5.3. Metric Selection.png" alt="Metric Selection" width="800" height="600" />
</p>

## 5.4. Result Delivery

<p align="justify">The delivery screen offers two options, each presented as a selectable card that expands to show its input:</p>

- **Receive by Email** — the results are compressed into a ZIP file and sent to the provided email address. A valid email format is required before proceeding.
- **Save Locally** — the user browses for a folder on their computer where the results will be saved.

<p align="center">
<img src="screenshots/5.4. Result Delivery.png" alt="Result Delivery" width="800" height="600" />
</p>

## 5.5. Confirmation 

<p align="justify">Before execution, all configured parameters are displayed in a summary card for review: analysis type, project name, CSV file path, test size, selected models, selected metrics, and delivery method. Clicking <strong>CONFIRM AND RUN</strong> saves the project to the database and starts the analysis.</p>

<p align="center">
<img src="screenshots/5.5. Confirmation.png" alt="Confirmation" width="800" height="600" />
</p>

## 5.6. Execution

<p align="justify">The execution screen shows the analysis running in real time. It contains four areas:</p>

- **Info bar** (top) — displays project name, analysis type, number of models, number of metrics, and elapsed time.
- **Log terminal** (left) — a color-coded log with timestamps. Messages are tagged as `[INFO]`, `[ OK ]`, `[ERR]`, or `[WARN]`.
- **Progress ring** (right) — a circular progress indicator showing the current completion percentage.
- **Pipeline tracker** (right) — lists the execution steps (Load CSV → Normalize → Split Data → Train Models → Evaluate → Save Results → Deliver), highlighting the active step and marking completed ones with a checkmark.

<p align="center">
<img src="screenshots/running.png" alt="Running Analysis" width="800" height="600" />
</p>

<p align="justify">When the analysis completes, a green success banner appears at the top with the total elapsed time. If the results were saved locally, the output path is shown along with an <strong>Open Folder</strong> button. A <strong>+ New Analysis</strong> button allows the user to start a new session.</p>

<p align="center">
<img src="screenshots/running_done.png" alt="Analysis Complete" width="800" height="600" />
</p>

## 5.7. Training Results

<p align="justify">The training analysis produces the following output files, organized into subfolders inside the project directory:</p>

- **Models/** — one `.pkl` file per trained model, ready for use in Prediction or Ensemble analyses.
- **Prediction/** — a CSV file with the gene classifications produced by each model on the test set.
- **Graphs/** — performance charts comparing the evaluation metrics across all trained models.

---

# 6. Prediction

## 6.1. Project Information

<p align="justify">After selecting <strong>Prediction</strong>, the Project Information screen requests a project name (5–10 characters), the CSV file with the data to be classified, and a previously trained model file in <code>.pkl</code> format.</p>

<p align="justify">If the selected model file is large, a feasibility check is performed automatically to verify that the system has sufficient RAM to load it.</p>

<p align="center">
<img src="screenshots/6.1. Project Information.png" alt="Project Information - Prediction" width="800" height="600" />
</p>

## 6.2. Result Delivery, Confirmation, and Execution

<p align="justify">The Delivery, Confirmation, and Execution screens follow the same structure as described in sections 5.4, 5.5, and 5.6. The pipeline tracker for Prediction shows the steps: Load CSV → Normalize → Predict → Save Results → Deliver.</p>

<p align="center">
<img src="screenshots/6.2. Result Delivery, Confirmation, and Execution.png" alt="Result Delivery, Confirmation, and Execution" width="800" height="600" />
</p>

## 6.3. Prediction Results

The prediction analysis produces a CSV file containing the classification (essential / non-essential) for each gene in the input dataset.

---

# 7. Ensemble

## 7.1. Project Information

<p align="justify">After selecting <strong>Ensemble</strong>, the Project Information screen requests a project name (5–10 characters), the CSV dataset for evaluation, a <strong>directory containing previously trained <code>.pkl</code> model files</strong>, and the test size proportion. The models in that directory are combined using a hard-voting strategy via scikit-learn's <code>VotingClassifier</code>.</p>

<p align="center">
<img src="screenshots/7.1. Project Information.png" alt="Project Information - Ensemble" width="800" height="600" />
</p>

## 7.2. Metric Selection

<p align="justify">The Ensemble wizard includes a metric selection step (same as Training, section 5.3) but skips individual model selection, since the models are loaded directly from the specified directory.</p>

## 7.3. Result Delivery, Confirmation, and Execution

<p align="justify">The Delivery, Confirmation, and Execution screens follow the same structure as described in sections 5.4, 5.5, and 5.6. The pipeline tracker for Ensemble shows: Load CSV → Normalize → Split Data → Aggregate Models → Evaluate → Save Results → Deliver.</p>

<p align="center">
<img src="screenshots/7.3. Result Delivery, Confirmation, and Execution.png" alt="7.3. Result Delivery, Confirmation, and Execution" width="800" height="600" />
</p>

## 7.4. Ensemble Results

The ensemble analysis produces:

- **Models/** — the combined VotingClassifier saved as a single `.pkl` file.
- **Prediction/** — a CSV file with the ensemble predictions on the test set.
- **Graphs/** — performance charts for the combined model.

---

# 8. Loading Existing Projects

<p align="justify">If projects of the same analysis type have been previously saved, the Project Information screen displays a segmented toggle at the top with two options: <strong>Create new</strong> and <strong>Load existing</strong>. Switching to <em>Load existing</em> shows a dropdown list of all saved projects for that type. Selecting a project loads all its previously configured parameters automatically, allowing the analysis to be re-run without re-entering information.</p>

<p align="center">
<img src="screenshots/8. Loading Existing Projects.png" alt="8. Loading Existing Projects" width="800" height="600" />
</p>

---

# 9. Prepare Dataset

<p align="justify">The dataset preparation module is accessible directly from the main window via the <strong>PREPARE DATASET</strong> button. It uses the bundled <code>prepareDataset2RNA.jar</code> module to convert raw genomic files into the CSV format accepted by GeneEssenceGUI. Java must be installed and available in the system PATH.</p>

Two preparation modes are available, each shown as a selectable card:

### Training Dataset

<p align="center">
<img src="screenshots/Training Dataset.png" alt="Training Dataset" width="800" height="600" />
</p>

Generates labeled CSV files for model training. Requires three inputs:

- **DEG annotation file** (`.csv`) — annotation file obtained from the DEG database, with at least 13 semicolon-separated columns.
- **FASTA file** (`.fasta`, `.fa`, or `.aa`) — amino acid sequences obtained from DEG.
- **GenBank directory** — a folder containing organism files in GenBank format (`.gb` / `.gbk`).

### Prediction Dataset

Generates the input file for the Prediction analysis. Requires one input:

- **GenBank directory** — a folder containing organism files in GenBank format.

<p align="center">
<img src="screenshots/Prediction Dataset.png" alt="Prepare Dataset" width="800" height="600" />
</p>

<p align="justify">After filling in all required fields, clicking <strong>NEXT</strong> starts the preparation. The execution screen displays a real-time log (dataset.log) with color-coded output. When the process completes, a success banner appears with the total time and an <strong>Open Folder</strong> button pointing to the output directory. Clicking <strong>+ New Preparation</strong> returns to the mode selection screen.</p>

<p align="center">
<img src="screenshots/Dataset Preparation Running.png" alt="Dataset Preparation Running" width="800" height="600" />
</p>
