# 🏠 Singapore Household Electricity Consumption Analysis 📊
*A data analysis project for NEA household electricity consumption*

## 🎯 Project Overview
This project implements a simple command-line query tool using data from Singapore's National Environment Agency (NEA) to analyze household electricity consumption patterns across different regions and dwelling types.

### 🔍 Key Features
- ⚡ Denormalized dataset generation from STAR schema using divide & conquer approach
- 🏘️ Multi-file data integration from various sources
- 📊 Command-line query interface for electricity usage analysis
- ⚙️ Multiple algorithm workings with time complexity analysis

## 🛠️ Technical Implementation
### Data Processing Pipeline
- `query.py`: Interactive query interface
- `complete.py`: Main data processing and integration
- Supporting algorithm and timing files

### Data
- Area data (AreaID, Area, Region)
- Dwelling types
- Electricity consumption records
- Date dimension (month, quarter, year)

## 🎮 How to Use
Run `python query.py`

![query preview](https://github.com/jaosy/AN6007-Electricity-Usage-Query-Tool/blob/main/query_example.png)
![timing preview](https://github.com/jaosy/AN6007-Electricity-Usage-Query-Tool/blob/main/timing_graph.png)
