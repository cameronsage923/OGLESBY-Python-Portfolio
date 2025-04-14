import streamlit as st
import spacy
from spacy.pipeline import EntityRuler
nlp = spacy.load("en_core_web_sm")
if "custom_patterns" not in st.session_state:
    st.session_state.custom_patterns = []

sample_texts = {
    "Famous Quote": "'The only thing we have to fear is fear itself.' - Franklin D. Roosevelt.",
    "Professor Review": "Professor Smiley is the greatest professor of all time!",
    "Diary Entry": "I really hate the Mendoza curve. It's ruining my life!",
    "Hinge Bio" : "I quote The Office like it's the Bible and still cry during every Deftones concert. If you like fried pickles or Crime Junky podcasts, we'll get along just fine."
}


st.title("🧠 Named Entity Recognition (NER) App")
st.markdown(
    """
    This app lets you explore Named Entity Recognition using **spaCy**, AND lets you customize it too!
    - Input your own text, or use one of the sample texts below.
    - Define custom entities, like "pickles" as FOOD (or BEST FOOD EVER if we're being real).
    - See your entities highlighted below!

    Created with L❤️VE using Streamlit and spaCy.
    """
)


st.subheader("Enter text below:")
st.subheader("Try a Sample Text")
selected_sample = st.selectbox(
    "Choose a sample (optional):",
    ["-- Select --"] + list(sample_texts.keys())
)

user_text = st.text_area(
    "Enter your text here or select a sample above:",
    value=sample_texts[selected_sample] if selected_sample in sample_texts else "",
    height=200
)

st.subheader("Define a Custom Entity (Optional)")
with st.form("custom_entity_form"):
    col1, col2 = st.columns(2)
    with col1:
        label = st.text_input("Enter the entity label (e.g., 'FOOD')")
    with col2:
        pattern = st.text_input("Enter the words or phrases to match (e.g., 'pickles')")
    add_rule = st.form_submit_button("Add Custom Rule")


if add_rule:
    if label and pattern:
        new_rule = {"label": label.upper(), "pattern": pattern}
        st.session_state.custom_patterns.append(new_rule)
        st.success(f"Added rule: '{pattern}' → {label.upper()}")
    else:
        st.warning("Please provide both a label and a pattern.")

# Add EntityRuler to the pipeline
if "entity_ruler" not in nlp.pipe_names:
    ruler = nlp.add_pipe("entity_ruler", before="ner")
else:
    ruler = nlp.get_pipe("entity_ruler")

# Add all stored custom patterns to the ruler
if st.session_state.custom_patterns:
    ruler.add_patterns(st.session_state.custom_patterns)
if st.button("Reset All Custom Rules"):
    st.session_state.custom_patterns = []
    st.success("All custom rules have been cleared.")

# If a custom rule was submitted
if add_rule and label and pattern:
    new_pattern = [{"label": label.upper(), "pattern": pattern}]
    ruler.add_patterns(new_pattern)
    st.success(f"Custom rule added: '{pattern}' as {label.upper()}")

# --- Display Results ---
from spacy import displacy

doc = nlp(user_text)
if not doc.ents:
    st.write("No named entities found.")
else:
    st.subheader("Visual Highlighting:")
    
    # Render HTML with displacy
    html = displacy.render(doc, style="ent", jupyter=False)
    
    # Display it in Streamlit using st.markdown and some CSS
    st.write("Entities highlighted in your text:")
    st.markdown(
        f"<div style='background-color: #f9f9f9; padding: 10px; border-radius: 8px;'>{html}</div>",
        unsafe_allow_html=True
    )
    st.subheader("Extracted Entities:")
    ent_data = [{"Text": ent.text, "Label": ent.label_} for ent in doc.ents]
    st.dataframe(ent_data)