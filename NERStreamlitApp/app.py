import streamlit as st
import spacy
from spacy.pipeline import EntityRuler

import spacy.cli
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


sample_texts = {
    "Party Invitation": "Lads, it's that time again. We're throwing down SATURDAY in the Keenan Courtyard. Theme: Shrek Rave. Come in green, bring a freind, leave with a memory (or at least a photo on someone's finsta). Fr. Dowd will be there, as well as former president Barack Obama, and rumor has it Breen-Phillips is making swamp punch. First 50 get free glow-in-the-dark rosaries. Be there or be excommunicated.",
    "Professor Review": "Professor Smiley is an icon. He once made a peanut butter & jelly sandwich with an entire loaf of Wonderbread to illustrate the importance of specific instructions. He loves Lord of the Rings and uses easter eggs to make class more fun. Though he is a full-time Python weapon these days, he used to be a comedian! What a guy.",
    "Diary Entry (Freshman Edition)": "I survived my first SYR. The theme was Barbenheimer and yes, I wore pink AND fake radiation goggles. My date spilled Spinelli’s ranch on my dress, but we still ended up in Dahnke. Tomorrow I have a finance quiz with Professor Ackerman and a group project for Professor Balko's class in Mendoza. Pray for me.",
    "Hinge Bio" : "I'm just a girl, standing in front of South Dining Hall, asking them to bring back decent mac and cheese. Also, shoutout to my therapist—aka the ducks at St. Mary’s Lake. I peaked during SYR season and now spend most of my days lurking in Debartolo Hall pretending to study. If you like fried pickles or Crime Junky podcasts, we'll get along just fine."
}

#st.image("NERimage.png", use_column_width=True)

st.title("🔍 Make Your Own NER: Label Like a Champion Today! ☘️ 💙")
st.markdown(
    """
    This app lets you explore Named Entity Recognition (NER) using **spaCy**, AND lets you define your own custom entities too! 
    How does it work?
    
    **Step 1:** Input your own text, or use one of the sample texts below.
    
    **Step 2:** Define custom entities, like "pickles" 🥒 as FOOD (or BEST FOOD EVER if we're being real).
    
    Finally, see your entities highlighted below!

    """
)


st.subheader("Choose a sample text, upload a file, or type your own text below:")
selected_sample = st.selectbox(
    "🗂️ Choose a sample (optional):",
    ["-- Select --"] + list(sample_texts.keys())
)

uploaded_file = st.file_uploader("📤 Or upload a .txt file:", type=["txt"])

user_text = ""

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    st.success("File is uploaded successfully!")
elif selected_sample in sample_texts:
    text = sample_texts[selected_sample]
else:
    text = ""

user_text = st.text_area("🖊️ Enter, view, and edit your text below:", value=text, height=200)
#################
##################
if "custom_patterns" not in st.session_state:
    st.session_state.custom_patterns = []

st.subheader("✍️ Define a Custom Entity (Optional):")
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

# Toggle to include/exclude spaCy's default NER
show_all_entities = st.checkbox("👁️ Check to Show ALL named entities (default + custom)!", value=True)

# Add EntityRuler and (optionally) remove default NER
if "entity_ruler" not in nlp.pipe_names:
    ruler = nlp.add_pipe("entity_ruler", before="ner" if "ner" in nlp.pipe_names else None)
else:
    ruler = nlp.get_pipe("entity_ruler")

# Optional: remove spaCy's default NER if toggle is off
if not show_all_entities and "ner" in nlp.pipe_names:
    nlp.remove_pipe("ner")

# Add custom patterns
if st.session_state.custom_patterns:
    ruler.add_patterns(st.session_state.custom_patterns)

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

# Display the list of custom rules if any exist
if st.session_state.custom_patterns:
    st.markdown("### 🧾 Your Custom Entity Rules")
    for i, rule in enumerate(st.session_state.custom_patterns, start=1):
        st.markdown(f"**{i}.** `{rule['pattern']}` : `{rule['label']}`")


# --- Display Results ---
from spacy import displacy
import streamlit.components.v1 as components

doc = nlp(user_text)
if not doc.ents:
    st.write("No named entities found.")
else:
    st.subheader("🔍 Recognized Entities:")
    ent_data = [{"Text": ent.text, "Label": ent.label_} for ent in doc.ents]
    st.dataframe(ent_data)

    st.subheader("👀 Visual Highlighting 👀:")
    
    st.subheader("📄 Full Text with Highlighted Entities:")

    # Get raw displacy HTML
    html = displacy.render(doc, style="ent", jupyter=False)

    # Inject a white background + padding directly into spaCy's internal container
    custom_html = html.replace(
        '<div class="entities"',
        '<div class="entities" style="background-color: white; padding: 20px; border-radius: 10px; font-family: Courier New, monospace; font-size: 16px;"'
    )
    components.html(custom_html, height=500, scrolling=True)

import matplotlib.pyplot as plt
import pandas as pd

# Only show chart if user has entered text
if user_text:
    doc = nlp(user_text)
    label_frequency = {}

    for ent in doc.ents:
        label_frequency[ent.label_] = label_frequency.get(ent.label_, 0) + 1

    if label_frequency:
        df = pd.DataFrame(label_frequency.items(), columns=["Entity Type", "Frequency"])
        df = df.sort_values("Frequency", ascending=False)

        # ND colors
        nd_colors = ["#0C2340", "#007A33", "#F3C613", "#004225", "#FFD100"]
        color_cycle = (nd_colors * (len(df) // len(nd_colors) + 1))[:len(df)]

        st.subheader("📊 Entity Frequency Charts")
        st.write("Expand the tabs below to visualize the breakdown and frequency of your named entities!")

        # Optional: use expanders or columns for layout
        with st.expander("📈 Bar Chart"):
            fig1, ax1 = plt.subplots()
            ax1.bar(df["Entity Type"], df["Frequency"], color=color_cycle)
            ax1.set_title("Named Entity Label Frequencies", fontsize=16, fontweight='bold')
            ax1.set_xlabel("Entity Type", fontsize=12)
            ax1.set_ylabel("Frequency", fontsize=12)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig1)

        with st.expander("🥧 Pie Chart"):
            fig2, ax2 = plt.subplots()
            ax2.pie(
                df["Frequency"],
                labels=df["Entity Type"],
                autopct='%1.1f%%',
                startangle=90,
                colors=color_cycle,
                textprops={'fontsize': 10, 'color': 'black'}
            )
            ax2.set_title("Entity Type Breakdown", fontsize=14, fontweight="bold")
            ax2.axis("equal")
            st.pyplot(fig2)
    else:
        st.info("No entities found to chart yet!")
else:
    st.info("👀 Enter some text above to see entity frequency results!")
