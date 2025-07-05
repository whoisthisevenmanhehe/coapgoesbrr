import streamlit as st
import json
import pandas as pd
from pathlib import Path

json_path = Path("cleaned_data.json")
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

standard_institutes = {
    "IISc Bangalore": ["iisc", "iisc bangalore", "iisc-blr", "iisc csa", "iiis-bangalore"],
    "IIT Bombay": ["iit bombay", "iitb", "iit-b", "iit b", "iit b cs", "iit b cs ta", "iit b mtech ta"],
    "IIT Delhi": ["iit delhi", "iit-delhi", "iit delhi cse", "iit delhi ctech", "iit delhi comp. tech", "iit delhi(ct)", "msr cse iit delhi", "iit delhi- ctech", "iit delhi comp. tech."],
    "IIT Kanpur": ["iit kanpur", "iitk", "iit kanpur cse", "iit kanpur-cse", "mtech cse iit kanpur", "kanpur", "m.tech cse ta kanpur(retained from r3)", "mtech cse iit kanpur ", "mtech cse iitkanpur"],
    "IIT Kharagpur": ["iit kgp", "iit kharagpur", "kgp", "iit kgp ai", "kgp ai", "kgp cs", "most probably kgp cse", "mostly accepting kgp cse", "iit kharagpur ai", "iitkh", "kharagpur cse", "iit kargp", "iit kharagpur(ai)", "[iit kgp] m.tech cse", "iit kharagpur cse retained", "iit kharagpur - computer science & engineering", "iit kharagpur - mtech cse", "qualify and reliability engineering iit kharagpur", "most prob iitkh ai", "iit kharagpur ai ", "iit kharagpur cs", "most prob iitkh"],
    "IIT Madras": ["iit madras", "iitm", "iit-m", "iit madras clinical", "iit madras cse", "iit madras mtech cse", "iit madras mtech cs", "iit madras mtech cse htta", "iit madras cse(htta)", "iit madras cse ", "accept and freeze iit madras"],
    "IIT Roorkee": ["iit roorkee", "roorkee mnc"],
    "IIT Hyderabad": ["iit hyderabad", "iith", "iit hyd", "mtech nis iit hyderabad", "iit hyd mtech ai", "iit hyderabad ai ta", "iit hyderabad cse accepted", "iit hyd cse", "iit hyd cs", "iit hyd nis", "iith nis"],
    "IIT Guwahati": ["iit guwahati", "iitg", "guwahati", "guw cse", "iit guwhati mtech cse", "iitg cs", "iitg (cs)", "iitg- cse", "iitg cse freeze", "mtech cse iit guwahati", "guwahati - cse", "iit guwahati cs", "iit guwahati cse ta", "iit guwahati m.tech cse", "mtech cse iit guwahati "],
    "IIT Gandhinagar": ["iit gandhinagar", "iit gn", "iit gandhinagar ai", "iit gandhinagr ai", "iit gandhinagar ai ", "iit gandhinagar cs", "iit gandhinagar cse", "iit gandhinagar cse "],
    "IIT Patna": ["iit patna", "iitp", "iit patna ai", "iitpatna ai", "mtech patna ai"],
    "IIT Ropar": ["iit ropar", "iit ropar cse", "iit ropar(cse)", "iit ropar "],
    "IIT BHU": ["iit bhu", "iit bhu - mtech ai", "iit bhu - mtech cse", "[iit bhu] cse-ai", "bhu cse", "bhu-iot", "bhu", "yet to decide(mostly bhu cse)"],
    "IIT Dhanbad": ["iit dhanbad", "ism dhanbad", "iitism dhanbad(ai&ds)", "iit dhanbad-cse", "ism dhanbad - ai&ds", "iit dhanbad cse"],
    "IIT Jodhpur": ["iit jodhpur", "iit jodhpur cse"],
    "IIT Indore": ["iit indore", "iit indore(cse)", "iit indore ms(r) cse", "iit indore mtech cse ta", "iit indore most probably"],
    "IIT Jammu": ["iit jammu", "iit jammu cse", "iit jammu mtech cse", "jammu cs", "iit jammu cse ta"],
    "IIT Bhilai": ["iit bhilai", "iit bhilai cse", "iit bhilai ds"],
    "IIT Bhubaneswar": ["iit bhubaneswar", "iit bbs", "iit bbs cse", "mtech iit bhubaneswar"],
    "IIT Dharwad": ["iit dharwad", "iit dharwad cs", "iit dharwad cse"]
}
st.set_page_config(page_title="COAP 2025 Explorer", page_icon="🎓", layout="wide")

alias_to_standard = {}
specialization_keywords = ["ai", "ds", "cyber", "nis"]

for std, aliases in standard_institutes.items():
    for alias in aliases:
        alias_to_standard[alias.strip().lower()] = std

junk_entries = set([
    "none", "no", "nan", "nill", "nil", "na", "n.a.", "nope", "reject", "rejected", "retain", "retain and wait",
    "not decided", "still thinking", "yet to decide", "t.b.d.", "thinking", "most likely reject", "accept", "accept and freeze",
    "thank god i am leaving this country for top ms school.", "i get only one offer per round bro", "confused", "currently thinking on it.",
    "i am yet to decide as i am confused", "most probably will accept", "general chaiwala", "most probably freeze it!"
])

def extract_institutes_from_string(value):
    if not isinstance(value, str):
        return []
    val = value.strip().lower()
    results = []
    for alias, std in alias_to_standard.items():
        if alias in val:
            results.append((std, next((s.upper() for s in specialization_keywords if s in alias or s in val), "CSE")))
    return list(set(results))

all_records = []
for round_name, records in data.items():
    for record in records:
        record["Round"] = round_name
        record["GATE Score"] = float(record.get("GATE Score", 0))
        record["GATE Rank"] = int(record.get("GATE Rank", 0))

        final_choices = extract_institutes_from_string(record.get("Offer selected to accept or retain", ""))
        round_offers = extract_institutes_from_string(record.get("M.Tech course work offers if received in this round - Please mention course name too", ""))
        research_offers = extract_institutes_from_string(record.get("Research offers if received in this round - Please mention specialization too", ""))

        record["Final Accepted Institute"] = ", ".join(sorted(set(i for i, _ in final_choices)))
        record["Final Accepted Specialization"] = ", ".join(sorted(set(s for _, s in final_choices)))
        record["Institutes Offered This Round"] = ", ".join(sorted(set(i for i, _ in round_offers)))
        record["Round Offer Specialization"] = ", ".join(sorted(set(s for _, s in round_offers)))
        record["Research Offer Institute"] = ", ".join(sorted(set(i for i, _ in research_offers)))
        record["Research Offer Specialization"] = ", ".join(sorted(set(s for _, s in research_offers)))

        all_records.append(record)

df = pd.DataFrame(all_records)

if "agreed" not in st.session_state:
    st.session_state.agreed = False

if not st.session_state.agreed:
    st.warning("⚠️ **Disclaimer**\n\nThe data used here is based on public contributions from [this Google Sheet](https://docs.google.com/spreadsheets/d/e/2PACX-1vSn_H-9XYgcLp02SjGKjYgFvT-ARzcTB91pWMb-i3d0OkfTCPM_eZ-5w_4Kxb2Sj8Uolq4CFM2mn2D9/pubhtml). While best efforts were made to clean and standardize it, the data **might not be fully accurate**. Please refer to official COAP documents for reliable information.\n\nThis tool is built just to help aspirants get a rough idea of trends.")

    if st.button("✅ I Understand, Continue"):
        st.session_state.agreed = True
        st.rerun()

    st.stop()

st.title("COAP 2025 Explorer - CS Stream")

st.sidebar.header("Filter Options")
rounds = sorted(df["Round"].unique(), key=lambda r: int(r.split()[-1]))
selected_round = st.sidebar.selectbox("Select Round", rounds, index=rounds.index("Round 1") if "Round 1" in rounds else 0)
institutes = sorted(set(i for val in df["Final Accepted Institute"].unique() for i in val.split(", ") if i))
selected_institute = st.sidebar.selectbox("Select Final Institute", ["All"] + institutes)

min_score, max_score = int(df["GATE Score"].min()), int(df["GATE Score"].max())
score_range = st.sidebar.slider("GATE Score Range", min_score, max_score, (min_score, max_score))

st.sidebar.markdown("""
<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" target="_blank">
    <button style="background-color:#f63366;color:white;border:none;padding:8px 16px;border-radius:8px;font-weight:bold;cursor:pointer;">I am telling you don't click me</button>
</a>
""", unsafe_allow_html=True)

filtered_df = df[df["Round"] == selected_round]
filtered_df = filtered_df[filtered_df["GATE Score"].between(score_range[0], score_range[1])]
if selected_institute != "All":
    filtered_df = filtered_df[filtered_df["Final Accepted Institute"].str.contains(selected_institute)]

st.subheader(f"Results for {selected_institute} in {selected_round} (GATE Score {score_range[0]} - {score_range[1]})")
st.dataframe(filtered_df.sort_values("GATE Rank", ascending=True)[[
    "GATE Rank", "GATE Score", "Category",
    "Institutes Offered This Round", "Round Offer Specialization",
    "Final Accepted Institute", "Final Accepted Specialization",
    "Decision for this round",
    "Research Offer Institute", "Research Offer Specialization", "Name",
    ]].reset_index(drop=True), use_container_width=True
)

st.markdown("### 📊 Statistics")
st.write("Total Records:", len(filtered_df))
if not filtered_df.empty:
    st.write("Average GATE Score:", round(filtered_df["GATE Score"].mean(), 2))
    st.write("First Rank (Lowest):", int(filtered_df["GATE Rank"].min()))
    st.write("Last Rank (Highest):", int(filtered_df["GATE Rank"].max()))
else:
    st.write("No data for selected filters.")

st.markdown("### 🏫 Final Institute Acceptances in Selected Round")

institute_counts = (
    df[df["Round"] == selected_round]["Final Accepted Institute"]
    .str.split(", ")
    .explode()
)
institute_counts = institute_counts[institute_counts.str.strip().ne("")]

institute_counts = institute_counts.value_counts().reset_index()
institute_counts.columns = ["Institute", "Accepted Count"]

#next year op will have his name in the list of round 1 with 900+ score ;)
if not institute_counts.empty:
    import plotly.express as px
    fig = px.bar(institute_counts, x="Institute", y="Accepted Count", text="Accepted Count", title=f"Offers and acceptance in {selected_round}")
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_title="Institute", yaxis_title="No. of Students")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No acceptance data available for this round.")

st.markdown("---")

st.markdown("""
    <div class="footer">
        📌 <b>Note</b>: Data from 
        <a href="https://docs.google.com/spreadsheets/d/e/2PACX-1vSn_H-9XYgcLp02SjGKjYgFvT-ARzcTB91pWMb-i3d0OkfTCPM_eZ-5w_4Kxb2Sj8Uolq4CFM2mn2D9/pubhtml" target="_blank">this sheet</a>. May contain inconsistencies. Please verify with official COAP docs.  
        <br>Built with 💮 to help COAP aspirants make informed decisions.
    </div>

    <img class="cat-gif" src="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" alt="funny cat">
""", unsafe_allow_html=True)
