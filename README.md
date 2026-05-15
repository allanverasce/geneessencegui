<p align="center">
  <img src="screenshots/genne_essence.png" alt="GeneEssenceGUI Logo" width="200" />
  <h1 align="center">GeneEssenceGUI</h1>
</p>



<p style="text-align: center;">Integrating DEG and NCBI datasets through ensemble machine learning for essential gene prediction</p>

<p style="text-align: center;">
  <a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white" alt="Python 3.12+" /></a>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" alt="Platform" />
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
- [2. Main Window](#2-main-window)
- [3. Dataset Format](#3-dataset-format)
- [4. Prepare Dataset](#4-prepare-dataset)
- [5. Analysis Type Selection](#5-analysis-type-selection)
- [6. Loading Existing Projects](#6-loading-existing-projects)

---

# 1. Installation

Two installation methods are available: running via Docker or running from source.

## 1.1. Docker

The `-v` flag mounts a folder from your machine into the container so that file dialogs inside the application can access your local files. Replace `/path/to/your/data` with the folder that contains your datasets and GenBank files. Inside the application, navigate to `/data` whenever a file or folder selection dialog appears.

### Linux
```bash
xhost +local:docker
docker run --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /path/to/your/data:/data \
  <dockerhub-user>/geneessencegui:v1.0.0
```

### macOS
Install [XQuartz](https://www.xquartz.org/) first, then:
```bash
xhost +localhost
docker run --rm \
  -e DISPLAY=host.docker.internal:0 \
  -v /path/to/your/data:/data \
  <dockerhub-user>/geneessencegui:v1.0.0
```

### Windows
Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) and start it with **Disable access control** checked, then:
```powershell
docker run --rm `
  -e DISPLAY=host.docker.internal:0 `
  -v C:\path\to\your\data:/data `
  <dockerhub-user>/geneessencegui:v1.0.0
```

## 1.2. From source

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

# 2. Starting the Application

<p align="justify">When GeneEssenceGUI starts, the main window is displayed. The left sidebar shows the tool name, a brief description, a list of the four available features, and the project partners. The right panel presents two buttons to begin:</p>

- **START ANALYSIS** — opens the analysis wizard (Training, Prediction, or Ensemble).
- **PREPARE DATASET** — opens the integrated dataset preparation module.

<p style="text-align: center;">
<img src="screenshots/3. Main Window.png" alt="Main Window" width="800" />
</p>

**Note**: If your dataset is suitable, you can proceed directly to the analysis type window (#5-analysis-type-selection)
---

# 3. Dataset Format

<p align="justify">GeneEssenceGUI requires datasets in CSV (Comma-Separated Values) format. Each row represents one gene instance. All columns except the last are treated as features; the <strong>last column must be the classification label</strong> (essential or non-essential).</p>

<p style="text-align: center;">
<img src="screenshots/2. Dataset Format.jpeg" alt="Dataset format example" width="600" />
</p>

Sample datasets are provided in the `datasets/` folder of this repository.

## Sample Datasets

The `datasets/` folder contains ready-to-use files for each analysis mode:

| File | Instances | Use |
|------|-----------|-----|
| `dataset1_toBuildModel.csv` | 73,324 | Training |
| `dataset2_toBuildModel.csv` | 25,601 | Training |
| `dataset_toBuildEnsemble.csv` | 98,925 | Ensemble |
| `validation_to_prediction.csv` | 893 | Prediction (labeled) |
| `validation.csv` | 893 | Prediction (unlabeled) |

All files share the same structure: **20 amino acid count features** (M, F, L, I, V, S, P, T, A, Y, H, Q, N, K, D, E, C, W, R, G) representing the residue composition of each gene product. In training and ensemble files the last column (`Product Name`) holds the gene product name sourced from the DEG database and serves as the classification label. Prediction files (`validation.csv`) omit this column since labels are unknown at inference time.

### `datasets/prepareDatasets/`

This sub-folder contains the raw genomic input files needed to reproduce the sample datasets using the **Prepare Dataset** module:

| File | Description |
|------|-------------|
| `DEG10.aa` | Amino acid FASTA file downloaded from DEG |
| `deg_annotation_p.csv` | DEG annotation file (semicolon-separated, ≥ 13 columns) |
| `genbank.zip` | GenBank files (`.gb`/`.gbk`) for the target organism — extract before use |

---

# 4. Prepare Dataset

<p style="text-align: justify;">The dataset preparation module is accessible directly from the main window via the <strong>PREPARE DATASET</strong> button. It uses the bundled <code>prepareDataset2RNA.jar</code> module to convert raw genomic files into the CSV format accepted by GeneEssenceGUI. Java must be installed and available in the system PATH.</p>

Two preparation modes are available, each shown as a selectable card:

### Training Dataset

<p style="text-align: center;">
<img src="screenshots/Training Dataset.png" alt="Training Dataset" width="800" />
</p>

Generates labeled CSV files for model training. Requires three inputs:

- **DEG annotation file** (`.csv`) — annotation file obtained from the DEG database, with at least 13 semicolon-separated columns.
- **FASTA file** (`.fasta`, `.fa`, or `.aa`) — amino acid sequences obtained from DEG.
- **GenBank directory** — a folder containing organism files in GenBank format (`.gb` / `.gbk`).

### Prediction Dataset

Generates the input file for the Prediction analysis. Requires one input:

- **GenBank directory** — a folder containing organism files in GenBank format.

<p style="text-align: center;">
<img src="screenshots/Prediction Dataset.png" alt="Prepare Dataset" width="800" />
</p>

<p style="text-align: justify;">After filling in all required fields, clicking <strong>NEXT</strong> starts the preparation. The execution screen displays a real-time log (dataset.log) with color-coded output. When the process completes, a success banner appears with the total time and an <strong>Open Folder</strong> button pointing to the output directory. Clicking <strong>+ New Preparation</strong> returns to the mode selection screen.</p>

<p style="text-align: center;">
<img src="screenshots/Dataset Preparation Running.png" alt="Dataset Preparation Running" width="800" />
</p>

---

# 5. Analysis Type Selection

<p style="text-align: justify;">Clicking <strong>START ANALYSIS</strong> opens the type selection screen. A progress sidebar on the left tracks the current step of the wizard, updating dynamically based on the type chosen. Three analysis types are available:</p>

- **Training** — trains one or more machine learning models on a labeled dataset. The wizard includes steps for model selection, metric selection, and delivery configuration.
- **Prediction** — applies a previously trained model (`.pkl`) to new data and returns the classification of each gene. The wizard goes directly from project setup to delivery configuration.
- **Ensemble** — combines multiple pre-trained models using a hard-voting strategy. Requires a directory containing `.pkl` model files. The wizard includes a metric selection step.

<p style="text-align: center;">
<img src="screenshots/4. Analysis Type Selection.png" alt="Analysis Type Selection" width="800" />
</p>

---

# 6. Loading Existing Projects

<p style="text-align: justify;">If projects of the same analysis type have been previously saved, the Project Information screen displays a segmented toggle at the top with two options: <strong>Create new</strong> and <strong>Load existing</strong>. Switching to <em>Load existing</em> shows a dropdown list of all saved projects for that type. Selecting a project loads all its previously configured parameters automatically, allowing the analysis to be re-run without re-entering information.</p>

<p style="text-align: center;">
<img src="screenshots/8. Loading Existing Projects.png" alt="9. Loading Existing Projects" width="800" />
</p>

# 7. Real-Time Task Monitoring

When you select any option, whether to perform training, run predictions, or load a previously created project, you will be automatically directed to the Running Analysis window.
In this window, you can monitor all ongoing tasks in real time. The progress of each step is displayed in two ways:

- Log Area Displays a detailed record of each step being executed, allowing you to track the status of all operations.
- Progress Bar Provides a visual indicator of the percentage of completed tasks, making it easy to estimate how much work remains.
  
*Note:* This feature ensures transparency and control over your workflow, keeping you informed about the status of all operations in progress.

<p style="text-align: center;">
<img src="screenshots/running.png" alt="10. Running" width="800" />
</p>



## License

AGPL-3.0 license — see [LICENSE](LICENSE) for details.
