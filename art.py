import streamlit as st
from streamlit_folium import st_folium
import folium
import time

st.set_page_config(page_title="Interactive Indian Art Map", layout="wide")

st.title("Interactive Indian Art Map — Art & Heritage across all States")
st.markdown(
    "Click markers to view a short description and image. Use the sidebar to filter by state or run the guided tour."
)

# --- Data: 1 representative art site per Indian state (28 states) ---
ART_SITES = [
    {"state":"Andhra Pradesh","site":"Amaravati Buddhist Stupa","city":"Amaravati","coords":[16.5417,80.5159],
     "desc":"Important archaeological and Buddhist art site known for ancient sculptures and reliefs.","img":"https://www.holidify.com/images/bgImages/AMARAVATHI.jpg"},
    {"state":"Arunachal Pradesh","site":"Tawang Monastery Art","city":"Tawang","coords":[27.5860,91.8649],
     "desc":"Monastery paintings, thangka art and ritual iconography of Tibetan-Buddhist tradition.","img":"https://easternroutes.com/wp-content/uploads/2017/12/Sela_Pass_Gate-Tawang-Arunachal_Pradesh.jpg"},
    {"state":"Assam","site":"Majuli Satra Arts","city":"Majuli","coords":[26.9566,94.1975],
     "desc":"Satras preserve dance, mask-making, performance arts and Assamese manuscript traditions.","img":"https://imagedelivery.net/y9EHf1toWJTBqJVsQzJU4g/www.indianholiday.com/2025/06/Majuli-Assam.jpg/w=750,h=428"},
    {"state":"Bihar","site":"Madhubani Painting","city":"Madhubani","coords":[26.3736,86.0713],
     "desc":"Famous folk-painting tradition with bold line work and bright natural pigments.","img":"https://amritadas.com/wp-content/uploads/2017/08/IMG_1365%C2%A9Amrita-Das.jpg"},
    {"state":"Chhattisgarh","site":"Bastar Tribal Crafts","city":"Jagdalpur","coords":[19.0728,82.0368],
     "desc":"Rich tribal metalwork, wood carving, bell-metal craft and mural traditions of Bastar.","img":"https://s7ap1.scene7.com/is/image/incredibleindia/chitrakote-water-falls-jagdalpur-chhattisgarh-1-attr-hero?qlt=82&ts=1727011277081"},
    {"state":"Goa","site":"Goan Church Art","city":"Panaji","coords":[15.4909,73.8278],
     "desc":"Colonial-era church architecture and Christian religious paintings influenced by Portuguese patronage.","img":"https://www.marefa.org/w/images/c/c0/Panjim%27s_Monuments.jpg"},
    {"state":"Gujarat","site":"Patan (Rani-ki-Vav) & Patola Textiles","city":"Patan","coords":[23.8500,72.1300],
     "desc":"Stepwell sculpture (Rani ki Vav) and the fine Patola weaving tradition of Gujarat.","img":"https://static.toiimg.com/thumb/99571977/Patan-in-Gujarat.jpg?width=636&height=358&resize=4"},
    {"state":"Haryana","site":"Kurukshetra—Sculptural Finds","city":"Kurukshetra","coords":[29.9699,76.8783],
     "desc":"Archaeological and religious art linked to ancient epics; local craft continuities.","img":"https://d3sftlgbtusmnv.cloudfront.net/blog/wp-content/uploads/2024/09/Places-To-Visit-In-Kurukshetra-Cover-Photo-840x425.jpg"},
    {"state":"Himachal Pradesh","site":"Kullu-Shivaratri & Pahari Paintings","city":"Kullu","coords":[31.7050,77.0990],
     "desc":"Pahari miniature painting schools, temple sculpture and festival arts in the hills.","img":"https://s7ap1.scene7.com/is/image/incredibleindia/chanderkhani%20pass-kullu-hp?qlt=82&ts=1726730672941"},
    {"state":"Jharkhand","site":"Rock Paintings & Tribal Art","city":"Ranchi","coords":[23.3441,85.3096],
     "desc":"Rock shelters and tribal painting / handloom traditions across Jharkhand.","img":"https://travelsetu.com/apps/uploads/new_destinations_photos/destination/2024/01/08/2f3f282a9bfcef08e3e93630853f7173_1000x1000.jpg"},
    {"state":"Karnataka","site":"Hampi — Vijayanagara Sculpture","city":"Hampi","coords":[15.3350,76.4600],
     "desc":"Vijayanagara-era architecture and stone sculpture; rich temple reliefs and inscriptions.","img":"https://www.holidaymonk.com/wp-content/uploads/2020/10/Vastuchitra_Stone-Chariot-Hampi.jpg"},
    {"state":"Kerala","site":"Kathakali & Mural Painting","city":"Thiruvananthapuram","coords":[8.5241,76.9366],
     "desc":"Classical dance-theatre (Kathakali), temple murals and traditional Kerala mural painting techniques.","img":"https://keralatourism.travel/images/destinations/headers/trivandrum-kerala-tourism-entry-fee-timings-holidays-reviews-header.jpg"},
    {"state":"Madhya Pradesh","site":"Khajuraho Temples","city":"Khajuraho","coords":[24.8316,79.9194],
     "desc":"World-famous medieval temple sculptures and narrative friezes celebrating art, spirituality and life.","img":"https://www.andbeyond.com/wp-content/uploads/sites/5/khajuraho-india-temple-complex.jpg"},
    {"state":"Maharashtra","site":"Ajanta & Ellora Caves","city":"Aurangabad","coords":[19.8762,75.3433],
     "desc":"Buddhist murals at Ajanta and multi-faith rock-cut architecture at Ellora are masterworks of Indian art.","img":"https://static.toiimg.com/photo/msid-52548490,width-96,height-65.cms"},
    {"state":"Manipur","site":"Manipuri Dance & Handloom","city":"Imphal","coords":[24.8170,93.9368],
     "desc":"Manipuri classical dance forms, vibrant handloom textiles and ritual performance arts.","img":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Imphal_view.jpg/500px-Imphal_view.jpg"},
    {"state":"Meghalaya","site":"Khasi & Jaintia Crafts","city":"Shillong","coords":[25.5788,91.8933],
     "desc":"Weaving, bamboo crafts and living musical & ritual traditions of the Khasi-Jaintia hills.","img":"https://etripto.in/uploads/0000/96/2023/06/29/wards-lake-shillong-photo-sanjukta-sharma.jpg"},
    {"state":"Mizoram","site":"Tribal Weaving & Crafts","city":"Aizawl","coords":[23.7271,92.7176],
     "desc":"Distinct tribal textiles, weaving motifs and festival arts in Mizoram.","img":"https://s7ap1.scene7.com/is/image/incredibleindia/aizawl-state-capital-mizoram-tri-hero?qlt=82&ts=1727165714611"},
    {"state":"Nagaland","site":"Hornbill Festival & Tribal Art","city":"Kohima","coords":[25.6751,94.1086],
     "desc":"Showcase of Naga textile motifs, wood carving, masks and performance arts at Hornbill festival.","img":"https://i.ytimg.com/vi/bod8bp7IESw/maxresdefault.jpg"},
    {"state":"Odisha","site":"Konark Sun Temple","city":"Konark","coords":[19.8876,86.0946],
     "desc":"13th-century temple famed for wheel-chariot motif and exquisite stone carvings.","img":"https://suryainn.in/wp-content/uploads/2023/09/konark-time-table.jpg"},
    {"state":"Punjab","site":"Golden Temple & Sikh Art","city":"Amritsar","coords":[31.6340,74.8723],
     "desc":"Sikh devotional art and architectural ornamentation epitomised in the Harmandir Sahib (Golden Temple).","img":"https://s7ap1.scene7.com/is/image/incredibleindia/1-sri-harmandir-sahib-(golden-temple)-amritsar-punjab-attr-hero?qlt=82&ts=1726662069037"},
    {"state":"Rajasthan","site":"Phad Paintings & Miniatures","city":"Jaipur","coords":[26.9124,75.7873],
     "desc":"Rajasthan’s miniature painting tradition, Phad scroll-paintings and palace arts.","img":"https://upload.wikimedia.org/wikipedia/commons/4/41/East_facade_Hawa_Mahal_Jaipur_from_ground_level_%28July_2022%29_-_img_01.jpg"},
    {"state":"Sikkim","site":"Rumtek & Buddhist Arts","city":"Gangtok","coords":[27.3389,88.6065],
     "desc":"Buddhist monasteries, thangka painting and Himalayan ritual arts concentrated in Sikkim.","img":"https://upload.wikimedia.org/wikipedia/commons/e/e8/Sikkim_Gangtok.jpg"},
    {"state":"Tamil Nadu","site":"Thanjavur (Tanjore) Paintings","city":"Thanjavur","coords":[10.7867,79.1378],
     "desc":"Tanjore paintings with gold leaf, temple iconography and South Indian classical sculpture.","img":"https://s7ap1.scene7.com/is/image/incredibleindia/1-ganaikondacholapuram-thanjavur-tamil-nadu-attr-hero?qlt=82&ts=1742170567992"},
    {"state":"Telangana","site":"Kalamkari & Kakatiya Sculpture","city":"Hyderabad","coords":[17.3850,78.4867],
     "desc":"Kalamkari textile painting, Kakatiya-era temple sculpture and Deccani painting influences.","img":"https://apacnewsnetwork.com/wp-content/uploads/2021/04/Hyderabad.jpg"},
    {"state":"Tripura","site":"Ujjayanta Palace & Tribal Art","city":"Agartala","coords":[23.8315,91.2868],
     "desc":"Traditional bamboo-cane work, tribal motifs and palace art in Tripura.","img":"https://upload.wikimedia.org/wikipedia/commons/2/2b/Tripura_State_Museum_Agartala_Tripura_India.jpg"},
    {"state":"Uttar Pradesh","site":"Varanasi / Banaras Art","city":"Varanasi","coords":[25.3176,82.9739],
     "desc":"Temple sculpture, Banarasi textiles, and the living ritual arts of India’s oldest city.","img":"https://s7ap1.scene7.com/is/image/incredibleindia/manikarnika-ghat-city-hero?qlt=82&ts=1727959374496"},
    {"state":"Uttarakhand","site":"Pahari Miniatures & Temple Art","city":"Nainital","coords":[29.3919,79.4542],
     "desc":"Pahari miniature painting schools and hill temple carvings found across Uttarakhand.","img":"https://www.cygnetthotels.com/blog/wp-content/uploads/2019/10/Picture1.png"},
    {"state":"West Bengal","site":"Shantiniketan & Bengal School","city":"Bolpur","coords":[23.6833,87.6833],
     "desc":"Rabindranath Tagore’s Santiniketan birthplace for the Bengal School of modern art and folk revival.","img":"https://i0.wp.com/buoyantlifestyles.com/wp-content/uploads/2019/02/28-1.jpg?resize=640%2C425&ssl=1"},
]

# --- Sidebar controls ---
st.sidebar.header("Filters & Controls")
all_states = sorted({s["state"] for s in ART_SITES})
selected_state = st.sidebar.multiselect("Select state(s)", options=all_states, default=all_states)

tour = st.sidebar.checkbox("Guided tour (auto step through sites)", value=False)
tour_speed = st.sidebar.slider("Tour delay (seconds)", 1.0, 5.0, 2.0)

# --- Build map centered on India ---
india_center = [22.0, 79.0]
m = folium.Map(location=india_center, zoom_start=5, tiles="OpenStreetMap")

# Colors to cycle through for markers
colors = ["red", "blue", "green", "purple", "orange", "darkred", "cadetblue"]

# Add markers for selected states
visible_sites = [s for s in ART_SITES if s["state"] in selected_state]

for i, site in enumerate(visible_sites):
    html = f"""
    <div style="width:280px">
      <h4 style="margin-bottom:6px">{site['site']}</h4>
      <img src="{site['img']}" width="260" style="display:block; margin-bottom:6px; border-radius:6px"/>
      <b>Location:</b> {site['city']}, {site['state']}<br/>
      <p style="margin-top:6px">{site['desc']}</p>
    </div>
    """
    iframe = folium.IFrame(html=html, width=300, height=260)
    popup = folium.Popup(iframe, max_width=300)

    folium.Marker(
        location=site["coords"],
        popup=popup,
        tooltip=f"{site['site']} — {site['state']}",
        icon=folium.Icon(color=colors[i % len(colors)], icon="info-sign")
    ).add_to(m)

# Fit map bounds to visible markers (if any)
if visible_sites:
    bounds = [s["coords"] for s in visible_sites]
    m.fit_bounds(bounds, padding=(30,30))

# --- Layout: map on left, list/details on right ---
left_col, right_col = st.columns((2,1))

with left_col:
    st.subheader("Map")
    st_data = st_folium(m, width=900, height=700)

with right_col:
    st.subheader("Selected Sites")
    st.write("Click a marker on the map to see details. Use filters to reduce the visible markers.")
    for i, s in enumerate(visible_sites):
        st.markdown(f"**{i+1}. {s['site']}** — *{s['city']}, {s['state']}*")
        st.caption(s["desc"])
        st.image(s["img"], use_container_width=True)

# --- Guided tour logic ---
if tour and visible_sites:
    st.sidebar.info("Starting guided tour — watch the map popup area update.")
    tour_placeholder = right_col.empty()
    for s in visible_sites:
        tour_placeholder.markdown(f"### Touring: {s['site']} — *{s['city']}, {s['state']}*")
        tour_placeholder.image(s["img"], use_container_width=True)
        tour_placeholder.write(s["desc"])
        time.sleep(tour_speed)
    st.sidebar.success("Tour finished.")

st.markdown("---")
st.markdown("**Notes:** This map is a starting point. You can expand each location with more images, bibliography, audio narration, or embed videos. If you want, I can export this dataset as CSV/JSON for use in KnightLab StoryMap or enhance it with timelines.")
