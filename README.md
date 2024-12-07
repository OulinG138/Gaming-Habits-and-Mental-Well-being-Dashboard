# Gaming Habits and Mental Well-being Dashboard

## Overview
This project features an **interactive dashboard** designed to explore the relationship between gaming habits and mental well-being. It provides insights into various factors such as gaming platforms, play styles, anxiety levels, and life satisfaction across different demographics. Explore the dashboard and its features at [here](https://sta313-project-5brqsj4nyusr65uvqvjcoq.streamlit.app/).

## Features
- Global visualization of gaming-related anxiety levels
- Age group analysis of gaming hours and anxiety scores
- Gaming platform distribution and player motivation analysis
- Quality of life correlations with gaming habits
- Interactive filters and detailed breakdowns

## Project Structure
```
├── assets
│   └── game_logos
├── data
│   ├── processed
│   │   └── processed_data.csv
│   └── raw
│       ├── Gaming Study Data.csv
│       └── world-countries.json
├── docs
│   └── Data Column Descriptions.pdf
├── notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_data_visualization.ipynb
├── src
│   ├── app.py
│   ├── components
│   │   ├── __init__.py
│   │   ├── age_groups.py
│   │   ├── bubble_chart.py
│   │   ├── game_chart.py
│   │   ├── life_quality.py
│   │   ├── player_motivation.py
│   │   ├── score_radar.py
│   │   ├── sunburst_chart.py
│   │   └── world_map.py
│   ├── pages
│   │   ├── __init__.py
│   │   ├── game_analysis.py
│   │   ├── player_analysis.py
│   │   └── quality_analysis.py
│   └── utils
│       ├── __init__.py
│       └── data_processing.py
```

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd STA313-Project
```

2. Create and activate a virtual environment:
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Or using pipenv
pipenv install
pipenv shell
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Ensure you're in the project's src directory:
```bash
cd src
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. The application will open in your default web browser at `http://localhost:8501`


## Usage
The dashboard consists of three main sections:

1. Kind of Player
   - Interactive world map showing anxiety levels by country
   - Age group analysis with gaming hours correlation
   - Player motivation analysis

2. Kind of Game
   - Platform distribution visualization
   - Gaming style analysis
   - Score comparisons across different platforms

3. Quality of Life
   - Correlation between gaming habits and life satisfaction
   - Demographic breakdowns
   - Mental well-being metrics

## Data Requirements
The application expects a CSV file with the following columns:
- GAD_T: General Anxiety Score
- SWL_T: Life Satisfaction Score
- Hours: Gaming Hours
- Platform: Gaming Platform
- Playstyle: Gaming Style
- Work: Employment Status
- Age: Player Age
- Residence_ISO3: Country Code
