### 🧠 Problem Definition – Marketing Analytics Project

Project Focus: Supermarket Bonus Card Program

### 🔍 Identify the Problem Area
This project focuses on Customer Retention and Market Segmentation, specifically within the context of a supermarket chain’s bonus card program. Sales have declined over the past year, prompting the need to understand customer behavior and loyalty patterns through analytics.

### 📚 Conduct Preliminary Research
Recent trends in retail emphasize personalization, loyalty programs, and data-driven segmentation. Bonus cards provide a rich data source that is often underutilized. Research suggests that poorly targeted offers and lack of customer engagement can reduce the effectiveness of such programs.

### 🎯 Define a Specific Problem
Despite having a bonus card system in place, the supermarket is experiencing declining sales.
Problem Statement:

“What factors are contributing to the drop in sales among bonus cardholders, and how can we use segmentation to improve customer retention and loyalty?”

### 🧠 Technologies Used
- **FastAPI** – Backend/API development  
- **Python** – Data processing and modeling  
- **Pandas, Scikit-learn** – ML and analytics  
- **PostgreSQL** – Database  
- **Streamlit / Figma** – UI prototype  
- **Git & GitHub Projects** – Version control and task tracking  

## 🧰 Project Setup & Instructions

### 📁 Clone the Repository

To get started, clone this repo using:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 🧪 Install Required Packages
There are multiple requirements.txt files for different components of the project. To install all dependencies, use the main file or install from each submodule as needed:

### Option 1: General installation (recommended for full environment)
```bash
# Clone the repository
git clone https://github.com/DS-223/Group-5.git
cd smartcrm

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Per-folder installation (modular development)
```bash
# For API
pip install -r app_components/api/requirements.txt

# For Data Science module
pip install -r app_components/ds/requirements.txt

# For ETL
pip install -r app_components/etl/requirements.txt

# For documentation (if using mkdocs)
pip install -r mkdocs_requirements.txt
```

### ⚙️ Run the Streamlit Front-End
To launch the front-end dashboard:

```bash
cd front
streamlit run App.py
```
If you encounter any missing packages, make sure the front-end requirements were installed.

### 🧬 Explore the ERD (Entity Relationship Diagram)
The project’s data model is based on a star schema. You can view the ERD under:

📄 ERD.pdf (included in the root directory)

It includes the following structure:

- **FactTransactions** (fact table)
- **DimDate, DimCustomer, DimCards** (dimension tables)

### 📁 Folder Structure

```bash
├── app_components
│   ├── api/                  # FastAPI backend
│   ├── ds/                   # Data science notebooks and scripts
│   └── etl/                  # ETL pipeline logic
├── └── front/                # Streamlit front-end
│       ├──pages/             # Streamlit multipage support
│       └── App.py            # Entry point for Streamlit app
├── └── .env                  # Environment variables
├── docs/                     # Documentation site (MkDocs)
├── feedback/                 # Instructor feedback files
├── docker-compose.yml        # Container orchestration
├── LICENSE
├── README.md
├── ERD.pdf                   # Entity Relationship Diagram
├── requirements.txt          # Global package requirements
```

### 👥 Team Roles

- **Project/Product Manager:** Albert Simonyan
- **Data Scientist:** Hayk Nalchajyan  
- **Backend Developer:** Gayane Hovsepyan  
- **Frontend Developer:** Mariam Mezhlumyan  
- **Database Developer:** Narek Ghukasyan 

---

### 📅 Milestones
- **Milestone 1:** Problem definition, roadmap, GitHub setup, UI prototype  
- **Milestone 2:** Database & model development, backend implementation  
- **Milestone 3:** Model integration, final dashboard, deployment 
