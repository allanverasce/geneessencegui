<p align="center">
  <img src="screenshots/genne_essence.png" alt="Logo" width="300" height="300" />
</p>

# <p align="center">GeneEssenceGUI: A user-friendly Python-based GUI for essential gene classification using machine learning</p>

<p align="justify"> DNA sequencing technologies have led to significant advances in knowledge about genetic content, from microorganisms to humans. One important analysis is annotation, i.e., the inference of biological information from genome sequences, which enables researchers to understand the function of genetic products, such as genes, the basic units of heredity responsible for physical and heritable traits. Some genes perform vital functions, encoding proteins or RNAs that are essential for processes such as cell metabolism and are involved in crucial pathways, including glycolysis and the tricarboxylic acid cycle. Sequencing platforms now produce large data volumes, driving advances in omics and the development of computational methods to support analysis. More recently, artificial intelligence and machine learning have been applied to this data, with studies showing the effectiveness of biology-inspired approaches. These models do not require rule-based programming, though their creation still demands advanced programming and computer skills. This study presents GeneEssenceGUI, a user-friendly Python-based GUI for essential gene classification using machine learning, implementing nine models to classify essential genes. The platform supports seamless data ingestion, model orchestration, and hyperparameter optimization through a unified graphical environment. GeneEssenceGUI implements a persistent SQLite-based storage system that logs all experimental metadata, ensuring full computational reproducibility and audit trails for genomic studies.</p>

### Technology 
<image src="https://github.com/user-attachments/assets/3406d50a-a37b-4980-976f-61d0cf916957" alt="Image" width="50" />
<image src="https://github.com/user-attachments/assets/5b44250e-ced9-46a6-84dd-a4954f408495" alt="Image" width="50" />
<img width="50" alt="image" src="https://github.com/user-attachments/assets/cb2a064a-069d-4dee-be39-b5829287257e" />

### Compatible with
<image src="https://github.com/user-attachments/assets/97a4af37-07f2-4283-ae7d-9a1db3e51d50" alt="Image" width="50"/>
<image src="https://github.com/allanverasce/allanverasce/assets/25986290/3f178481-786d-4e6f-b46f-7e10732e9ca8" alt="Image" width="50"/>
<img width="50" height="50" alt="image" src="https://github.com/user-attachments/assets/839d6c26-8c29-48a2-ac95-29be48d066bd" />

# Installation and User Guide 
<p align="justify">To run GeneEssenceGUI, you must install Python 3.12 or higher on your system. The installer can be obtained from the official website: Download Python.</p>

### Windows Installation
1. Download the Python installer (python-12.x.x.exe) from the official website.
2. Run the installer and check "Add Python to PATH" before proceeding.
3. Click "Install Now" and wait for the installation to complete.
4. Verify the installation by opening the command Prompt and running: python --version

### Linux Installation (Ubuntu/Debian-based)
1. Update the package list: sudo apt update && sudo apt upgrade -y
2. Install Python using apt: sudo apt install python3
3. Verify the installation: python3 --version

### macOS Installation
1. Install Homebrew (if not already installed): /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
3. Install Python using Homebrew: brew install python
4. Verify the installation: python3 --version

## Running the software
<p>After downloading, follow the instructions according to your operating system: </p>

### Linux and macOS
- Grant execute permissions to the downloaded file:
``` 
chmod 777 GeneEssenceGUI
```

- For Linux: Double-click the file or run it in the terminal:

```
./GeneEssenceGUI
```

- For macOS: It is necessary to execute it through the terminal:

```
./GeneEssenceGUI
```
- Windows: Right-click on the executable and select "Run as administrator". This ensures the software has the necessary permissions to access system resources, preventing execution errors and enhancing compatibility with dependencies.

## Dataset Model
<p align="justify">For GeneEssenceGUI to function correctly, the dataset shown in Figure 1 must be in CSV (Comma-Separated Values) format. This format organizes data into rows and columns, each representing a data instance and containing a characteristic gene variable. To simplify data preparation, we provide a processing script that converts your files into the format the software accepts.</p>
<p align="center">
<img src="screenshots/figure3.jpeg" alt="Logo" width="600" height="500" />
</p>

## Main Window
<p align="justify">When you start running the software, the GeneEssenceGUI main window appears below. The window contains a welcome message and a brief description of the tool's main features, along with information about the partners involved in the project. To start using the software, click the "Start" button.</p>

<p align="center">
<img src="screenshots/mainW.png" alt="Logo" width="800" height="600" />
</p>


