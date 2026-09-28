Fermi-Level and Defect-Energy Prediction with Machine Learning

A computational materials science project combining Density Functional Theory (DFT) calculations and machine learning (ML) to investigate electronic properties of transition-metal-doped iron surfaces and predict material properties from computationally derived descriptors.

Overview

Understanding how atomic substitutions and defects influence the electronic structure of materials is important for designing catalysts and functional materials.

In this project, I investigate transition-metal-doped Fe surfaces using atomistic simulations and machine learning. DFT calculations are used to generate electronic-structure data, which are then processed into machine-learning features for predicting properties such as the Fermi level and defect-related energies.

The project demonstrates a workflow connecting:

Atomic structure → DFT calculations → Feature generation → Machine learning → Property prediction

Research Motivation

Iron-based materials are relevant to catalytic processes, including reactions involving CO₂ adsorption and conversion. Introducing different transition-metal dopants can modify the electronic structure of the Fe surface and potentially influence its interaction with adsorbates.

The main questions explored in this project are:

* How does transition-metal doping affect the Fermi level of Fe surfaces?
* Can machine learning learn relationships between atomic/material descriptors and calculated electronic properties?
* Can ML models be used to predict electronic properties of structures that have not been explicitly calculated?
* How can computational materials science and ML be combined to accelerate materials screening?

Computational System

The main system studied consists of transition-metal-doped bcc Fe surfaces.

Surface orientations

* Fe(100)
* Fe(110)
* Fe(111)

Model construction

The calculations include:

* Fe surface slabs
* Transition-metal dopants
* Periodic boundary conditions
* Vacuum regions separating periodic slabs
* Spin-polarized electronic-structure calculations

The dataset contains approximately 96 generated doped structures, with 95 structures retained after data cleaning.

Density Functional Theory

DFT calculations were performed using computational chemistry/materials-science packages including:

* GPAW
* Quantum ESPRESSO
* ASE

The calculations primarily use:

* PBE exchange-correlation functional
* Spin polarization
* Plane-wave calculations
* A 350 eV plane-wave cutoff for the relevant calculations
* 3 × 3 × 3 k-point sampling for the computational setup

The DFT calculations provide electronic-structure quantities that are subsequently used to construct the machine-learning dataset.

Machine Learning Workflow

The ML workflow involves extracting chemically meaningful descriptors from the calculated structures and training regression models to predict target properties.

Descriptor generation

Material and atomic descriptors were generated using tools including:

* Matminer
* JARVIS-ML
* pymatgen

The initial feature space contains approximately 87 descriptors, which were subsequently processed and reduced for model development.

The final models use a smaller set of selected descriptors, including descriptors related to properties such as:

* Electronegativity
* Heat of fusion
* Atomic/material properties
* JARVIS-derived descriptors

Machine Learning Models

Several machine-learning approaches are explored, including:

* Decision Tree Regression
* Random Forest Regression
* K-Nearest Neighbors (KNN)

The models are evaluated using standard regression metrics to investigate how accurately the electronic properties can be predicted from the calculated descriptors.

Example result

The Random Forest model achieved approximately 81% explained variance for the investigated Fermi-level prediction task, with a reported deviation of approximately 0.2893 under the corresponding evaluation setup.

These results indicate that machine-learning models can capture meaningful relationships between material descriptors and the calculated electronic properties within the dataset.

Note: Model performance is dataset- and evaluation-dependent. The relatively small dataset means that the results should be interpreted as a proof-of-concept rather than a definitive demonstration of generalization to arbitrary materials.

Project Workflow

Transition-metal dopants
          │
          ▼
   Build Fe surface
      structures
          │
          ▼
     DFT calculations
    (GPAW / QE / ASE)
          │
          ▼
 Electronic-structure data
          │
          ▼
 Feature / descriptor
      generation
          │
          ▼
 Feature selection
          │
          ▼
 Machine-learning models
          │
     ┌────┼────┐
     ▼    ▼    ▼
    DT    RF   KNN
     │    │    │
     └────┼────┘
          ▼
 Property prediction
          │
          ▼
 Model evaluation

Tools and Technologies

Computational Chemistry / Materials Science

* ASE
* GPAW
* Quantum ESPRESSO
* pymatgen
* Matminer
* JARVIS

Machine Learning / Data Science

* Python
* NumPy
* Pandas
* Scikit-learn
* Matplotlib

Installation

Clone the repository:

git clone https://github.com/YakubuNaat/fermi-level-and-defect-energy-prediction-with-ml.git
cd fermi-level-and-defect-energy-prediction-with-ml

Create a Python environment:

python -m venv venv
source venv/bin/activate

Install the required Python packages:

pip install -r requirements.txt

Some DFT calculations require additional installation and configuration of GPAW and/or Quantum ESPRESSO. Their installation requirements depend on the computing environment.

Reproducibility

The project is organized to separate:

1. Structure generation
2. DFT calculations
3. Data extraction
4. Descriptor generation
5. Machine-learning analysis

This separation makes it possible to reproduce individual stages of the computational workflow without rerunning the entire project.

For large DFT outputs and computational data, only selected files may be included in this GitHub repository. Large datasets and calculation outputs can be stored separately when necessary.

Future Work

Potential extensions of this project include:

* Increasing the size and chemical diversity of the dataset
* Exploring additional transition-metal dopants
* Investigating CO₂ adsorption on doped Fe surfaces
* Predicting adsorption energies using ML
* Testing additional machine-learning algorithms
* Hyperparameter optimization
* Uncertainty estimation
* Explainable machine learning
* Comparing different surface orientations
* Incorporating additional electronic-structure descriptors
* Using larger public materials databases for model training
* Exploring graph-based and deep-learning approaches for atomistic materials

Research Context

This project was developed as part of my broader interest in computational chemistry, materials science, machine learning, and computational catalysis.

The long-term goal is to explore how computational simulations and data-driven methods can be combined to accelerate the discovery and screening of materials for applications such as catalysis and CO₂ conversion.

Author

Yakubu Abdulai

BSc Chemistry — Kwame Nkrumah University of Science and Technology (KNUST)

Research interests:

* Computational Chemistry
* Materials Science
* Density Functional Theory
* Machine Learning for Materials
* Computational Catalysis
* CO₂ Capture and Conversion
* Electronic-Structure Modeling

GitHub: @YakubuNaat

Disclaimer

This repository is primarily a research and portfolio project. The reported machine-learning performance reflects the specific dataset, descriptors, models, and evaluation procedure used in the project and should not be interpreted as a universal predictive model for Fe-based materials.
