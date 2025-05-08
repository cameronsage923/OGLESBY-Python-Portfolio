# Named Entity Recognition (NER) App 🧠 
Welcome! This is an interactive NLP web app built with **Streamlit** and **spaCy** that lets users experiment with Named Entity Recognition (NER) and define custom entities using `EntityRuler`. Upload your own text, add domain-specific labels, and visualize entity patterns in real time.

---

## 📊 Project Overview

This interactive web app allows users to explore Named Entity Recognition (NER) using [spaCy](https://spacy.io/)'s NER pipeline. Users can:
- Upload or type any body of text (or use a fun sample provided)
- Explore pre-trained NER labels such as `PERSON`, `ORG`, `DATE`, `GPE`, etc.
- Add custom entity rules to tag domain-specific terms (e.g., `"Spinelli's ranch"` as `FOOD`)
- Visualize results with live highlighting and frequency charts
It combines statistical modeling and rule-based logic, offering an educational and customizable introduction to applied NLP.

---

## 🧠 Skills & Technologies Used
- Python
- Streamlit
- spaCy
- `en_core_web_sm` model
- Custom rule-based `EntityRuler`
- Interactive charting via `matplotlib` and `pandas`

## 📸 App Previews
Entity Highlighting:
<img width="509" alt="NERexample" src="https://github.com/user-attachments/assets/a2dbd3eb-b4e4-4499-a289-39082ce90517" />

Entity Frequency Charts:
<img width="502" alt="NERchartexample" src="https://github.com/user-attachments/assets/1e22085a-6efd-40e5-85ef-c7062f3a51b4" />

## 🌐 Live Demo
Try it out here: [NER App on Streamlit Cloud](https://namedentityrecognitionapp.streamlit.app/) 

### 🚀 Or Run the App Locally
First, ensure you have **Python 3.8+** installed along with the required libraries. You can install dependencies using:
```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
Then, clone the repository and run the app from your terminal:
```bash
   git clone https://github.com/cameronsage923/OGLESBY-Python-Portfolio/NERStreamlitApp.git
   cd NERStreamlitApp
   streamlit run app.py
   ```

---

## 🔗 References

- [spaCy Documentation](https://spacy.io/usage)
- [EntityRuler Component](https://spacy.io/api/entityruler)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [spaCy Visualizer – displacy](https://spacy.io/usage/visualizers)

---

