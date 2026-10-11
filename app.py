import re
import streamlit as st

st.set_page_config(page_title="Customer Info", page_icon="📝", layout="centered")

st.markdown(
    """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 2rem; max-width: 520px;}
    </style>
    """,
    unsafe_allow_html=True,
)

FIELDS = [
    ("Name", "f_name"),
    ("Contact", "f_contact"),
    ("Building Name", "f_building"),
    ("Floor", "f_floor"),
    ("Road Name", "f_road_name"),
    ("Road Number", "f_road_no"),
    ("Block/Sector", "f_block"),
    ("Area", "f_area"),
]
BILLING_KEY = "f_billing"
ALL_KEYS = [k for _, k in FIELDS] + [BILLING_KEY]

for k in ALL_KEYS:
    st.session_state.setdefault(k, "")


def remove_all():
    for k in ALL_KEYS:
        st.session_state[k] = ""
    st.session_state.pop("saved_text", None)
    st.session_state.pop("saved_name", None)


def build_text():
    lines = [f"{label} : {st.session_state[key].strip()}" for label, key in FIELDS]
    lines.append(f"Details Billing Info : {st.session_state[BILLING_KEY].strip()}")
    return "\n".join(lines) + "\n"


st.markdown("### Customer Info")

for label, key in FIELDS:
    if key == "f_area":
        st.text_area(label, key=key, height=130)
    else:
        st.text_input(label, key=key)
st.text_area("Details Billing Info", key=BILLING_KEY, height=130)

c1, c2 = st.columns(2)
save_clicked = c1.button("Save", type="primary", use_container_width=True)
c2.button("Remove all", on_click=remove_all, use_container_width=True)

if save_clicked:
    name = st.session_state["f_name"].strip()
    if not name:
        st.warning("Name likho, tarpor Save dao.")
        st.session_state.pop("saved_text", None)
    else:
        safe = re.sub(r'[\\/:*?"<>|]+', "_", name)
        st.session_state.saved_text = build_text()
        st.session_state.saved_name = f"{safe}.txt"

if st.session_state.get("saved_text"):
    st.success("Save hoyeche. Niche button e tap kore Notepad file ta nao.")
    st.download_button(
        "Download Notepad file (.txt)",
        data=st.session_state.saved_text.encode("utf-8-sig"),
        file_name=st.session_state.saved_name,
        mime="text/plain",
        use_container_width=True,
    )
