import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MiniMap
import pandas as pd
import time
import math
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Tourist Planner",
    page_icon="✈️",
    layout="wide"
)

st.markdown(
    '<p class="title">🌍 Smart Tourist Planner</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub">Plan Your Dream ✈️💰</p>',
    unsafe_allow_html=True
)
# ---------------- CITY DATA ----------------
city_data = {
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "Goa": {"lat": 15.2993, "lon": 74.1240},
    "Manali": {"lat": 32.2432, "lon": 77.1892},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Kerala": {"lat": 10.8505, "lon": 76.2711},
    "Dubai": {"lat": 25.2048, "lon": 55.2708},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Maldives": {"lat": 3.2028, "lon": 73.2207}
}

tourist_places = {
    "Goa": ["Baga Beach", "Anjuna Beach", "Fort Aguada"],
    "Manali": ["Solang Valley", "Rohtang Pass", "Hadimba Temple"],
    "Jaipur": ["Hawa Mahal", "Amer Fort", "City Palace"],
    "Kerala": ["Munnar", "Alleppey", "Thekkady"],
    "Dubai": ["Burj Khalifa", "Dubai Mall", "Palm Jumeirah"],
    "Singapore": ["Marina Bay Sands", "Sentosa Island", "Gardens By The Bay"],
    "Maldives": ["Male City", "Vaadhoo Island", "Banana Reef"]
}


with st.sidebar.form("trip_form"):
    destination_cities = [city for city in city_data.keys() if city != "Ahmedabad"]
    to_city = st.selectbox("🏖 To City", destination_cities)
    num_travelers = st.number_input("👨‍👩‍👧 Number of Travelers", 1, 10, 1)
    num_days = st.number_input("📅 Number of Days", 1, 30, 5)
    budget = st.select_slider("💰 Budget", options=["Low","Medium","High"])
    mode = st.selectbox("🛣️ Transport Mode",["--Select--","🚗 Car","🚆 Train","✈️ Airplane"])

    submit = st.form_submit_button("🚀 Continue")
if "show_budget" not in st.session_state:
    st.session_state.show_budget = False
# ---------------- DISTANCE FUNCTION ----------------
def calculate_distance(lat1, lon1, lat2, lon2):
    return round(math.sqrt((lat2-lat1)**2 + (lon2-lon1)**2) * 111, 2)

# ---------------- LOCATION ----------------
from_lat = city_data["Ahmedabad"]["lat"]
from_lon = city_data["Ahmedabad"]["lon"]

to_lat = city_data[to_city]["lat"]
to_lon = city_data[to_city]["lon"]

distance = calculate_distance(
    from_lat,
    from_lon,
    to_lat,
    to_lon
)

if submit: 
    with st.spinner("Calculating budget..."): 
        time.sleep(2) 
        st.session_state.show_budget = True
if st.session_state.show_budget:
    if mode == "--Select--":
        if budget == "Low":
            transport = "🚆 Train"
            travel_cost_per_km = 2

        elif budget == "Medium":
            transport = "🚗 Car"
            travel_cost_per_km = 5
        else:
            transport = "✈️ Airplane"
            travel_cost_per_km = 10

    else:
    
        transport = mode
        if transport == "🚆 Train":
            travel_cost_per_km = 2
        elif transport == "🚗 Car":
            travel_cost_per_km = 5
        elif transport == "✈️ Airplane":
            travel_cost_per_km = 10
    if budget == "Low":
    
        hotel_per_day = 1200
        food_per_day = 500
    elif budget == "Medium":
    
        hotel_per_day = 3000
        food_per_day = 1000
    else:
    
        hotel_per_day = 7000
        food_per_day = 2500
    hotel = hotel_per_day * num_days * num_travelers
    food = food_per_day * num_days * num_travelers
    travel = distance * travel_cost_per_km * num_travelers
    shopping = (hotel + food + travel) * 0.15
    inr_budget = hotel + food + travel + shopping
    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(["Info","Song","Video","Bill","Chart","Map"])

    with tab1:
        st.subheader(f"🏟️ Welcome to {to_city}")
        destination_info = {
            "Goa": "Famous for beaches, nightlife and water sports.",
            "Manali": "A beautiful hill station surrounded by mountains.",
            "Jaipur": "The Pink City known for forts and royal heritage.",
            "Kerala": "Known as God's Own Country with backwaters and greenery.",
            "Dubai": "A modern city famous for luxury, shopping and skyscrapers.",
            "Singapore": "A clean and futuristic city with world-class attractions.",
            "Maldives": "A tropical paradise famous for islands and resorts."
        }
        st.info(destination_info[to_city])
        st.subheader("📊 Trip Overview")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("📍 Distance", f"{distance} KM")
        with col2:
            st.metric("👨‍👩‍👧 Travelers", num_travelers)
        with col3:
            st.metric("📅 Days", num_days)
        with col4:
            st.metric("💰 Budget", budget)
        with col5:
            if mode == "--Select--":
                st.metric("🚘 Transport", "Auto")
            else:
                st.metric("🚘 Transport", mode)
        st.divider()
        st.subheader("🌴 Top Tourist Attractions")
        for place in tourist_places[to_city]:
            st.write(f"✅ {place}")
        st.divider()
        foods = {
            "Goa": ["Fish Curry", "Bebinca", "Prawn Balchão"],
            "Manali": ["Siddu", "Trout Fish", "Babru"],
            "Jaipur": ["Dal Baati Churma", "Ghewar", "Kachori"],
            "Kerala": ["Appam", "Puttu", "Kerala Fish Curry"],
            "Dubai": ["Shawarma", "Machboos", "Luqaimat"],
            "Singapore": ["Hainanese Chicken Rice", "Laksa", "Chilli Crab"],
            "Maldives": ["Mas Huni", "Garudhiya", "Bis Keemiya"]
        }
        st.subheader("🍽️ Famous Foods")
        for i in foods[to_city]:
            st.write(f"🍴 {i}")
        st.divider()
        best_time = {
            "Goa": "October - March",
            "Manali": "March - June",
            "Jaipur": "October - March",
            "Kerala": "September - March",
            "Dubai": "November - March",
            "Singapore": "February - April",
            "Maldives": "November - April"
        }
        st.subheader("📅 Best Time To Visit")
        st.success(best_time[to_city])
        st.divider()
        st.subheader("💡 Travel Tips")
        tips = [
            "Carry a    valid ID proof.",
            "Keep emergency cash available.",
            "Book hotels in advance.",
            "Stay hydrated during travel.",
            "Keep your mobile fully charged."
        ]
        for tip in tips:
            st.write(f"✅ {tip}")

    with tab2:
        st.subheader(f"🎵 Travel Songs For {to_city}")

        spotify_tracks = {
            "Goa": [
                "2r1CHpKRDdzHGJScn5UqjX",
                "723xQva0yBF7M6K3nDAG8R",
                "7oLBAjVbhu5m0wG32xqSwC"
            ],

            "Manali": [
                "1kcV2LJxt5v0s2cEGtEJ5i",
                "14eotumM24MhIgzidgN3Jx",
                "4mIFaN3SWgBJlLjnyAMeg4"
            ],

            "Jaipur": [
                "6VBhH7CyP56BXjp8VsDFPZ",
                "2Wu9PNpLUCBl3W1GaPqkh",
                "4eFnk661RcdOuH9ajiTO3j"
            ],

            "Kerala": [
                "14eotumM24MhIgzidgN3Jx",
                "6w458kA8WOAIZr1ublxnK9",
                "5cgKosPPj5Cs9a2JQufUc1"
            ],

            "Dubai": [
                "0ct6r3EGTcMLPtrXHDvVjc",
                "0VjIjW4GlUZAMYd2vXMi3b",
                "39LLxExYz6ewLAcYrzQQyP"
            ],

            "Singapore": [
                "2xFg6AyHkXFruGxRjy7Uzn",
                "0ct6r3EGTcMLPtrXHDvVjc",
                "39LLxExYz6ewLAcYrzQQyP"
            ],

            "Maldives": [
                "1D35BJlymlh6OLD75WupSF",
                "0snQrp1VaY5Pj1YIHRJpRJ",
                "0eLtIxPRNJfsmehITZ1qaJ"
            ]
        }

        for track_id in spotify_tracks[to_city]:
            components.html(
                f"""
                <iframe
                    style="border-radius:12px"
                    src="https://open.spotify.com/embed/track/{track_id}"
                    width="100%"
                    height="150"
                    frameborder="0"
                    allowfullscreen=""
                    allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
                    loading="lazy">
                </iframe>
                """,
                height=150
            )
    with tab3:
        st.subheader("🎥 Best Travel Videos")
    
        # Real verified YouTube video IDs
        videos = {
            "Goa": [
                ("🌊 Goa Complete Travel Guide", "626iPtnK_MA", "Travel Guide"),
                ("🏖 Goa Beaches & Vibes", "Hs-KdhM9Jb8", "Beaches"),
                ("🎬 Goa Trip in 4K", "cBbS8Pi0obo", "4K Cinematic"),
            ],
            "Manali": [
                ("🏔 Manali Complete Travel Guide", "vb6USc_YCLA", "Travel Guide"),
                ("❄️ Manali Winter Snow Trip", "qS6EFgOlMKk", "Winter"),
                ("🚵 Manali Rohtang Pass", "Q8jzA5I8Y_Q", "Adventure"),
            ],
            "Jaipur": [
                ("🏰 Jaipur Travel Guide", "H0zRZgB9r_w", "Travel Guide"),
                ("👑 Amer Fort Full Tour", "lLQ1gPPGkpg", "Heritage"),
                ("📸 Jaipur Pink City in 4K", "BDq5QOaFHrY", "4K Cinematic"),
                ("🎨 Jaipur Food & Culture", "Ql5E9oUBMBY", "Food & Culture"),
            ],
            "Kerala": [
                ("🌴 Kerala Travel Guide", "ObRkZ8lMZOo", "Travel Guide"),
                ("🚣 Alleppey Backwaters Houseboat", "Bg_DkpCX43o", "Backwaters"),
                ("⛰ Munnar Tea Gardens", "KDpU5CQOZR0", "Nature"),
                ("🌿 Kerala — God's Own Country", "kBJkxbqMGAw", "Cinematic"),
            ],
            "Dubai": [
                ("🌆 Dubai Travel Guide 2024", "UoTK5G9uBOI", "Travel Guide"),
                ("🏙 Burj Khalifa Experience", "6KFaRJKJQBk", "Landmark"),
                ("🛍 Dubai Mall Mega Tour", "KQ0kLRFRXcE", "Shopping"),
                ("✨ Dubai in 4K Cinematic", "TCmLEeNQMzs", "4K Cinematic"),
            ],
            "Singapore": [
                ("🌃 Singapore Travel Guide", "P_bsMqtFglY", "Travel Guide"),
                ("🌺 Gardens by the Bay Night", "TK0rBjNP2KY", "Gardens"),
                ("🎡 Sentosa Island Full Tour", "uNXFMlpMWmo", "Leisure"),
                ("🏙 Singapore in 4K", "4TBGm2oAG3M", "4K Cinematic"),
            ],
            "Maldives": [
                ("🏝 Maldives Travel Guide", "3OFmFOohlX8", "Travel Guide"),
                ("🌊 Maldives Overwater Resort", "H2fHMpb7aBQ", "Resort"),
                ("🐠 Maldives Underwater World", "2d1OUPQo4KA", "Diving"),
                ("☀️ Maldives in 4K", "kj3ePhW9oaA", "4K Cinematic"),
            ],
        }
    
        st.info(f"🔥 Top Travel Videos For **{to_city}**")
    
        city_videos = videos.get(to_city, [])
    
        # Render in a 2-column card grid
        cols = st.columns(2)
        for i, (title, vid_id, label) in enumerate(city_videos):
            thumb = f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg"
            url = f"https://www.youtube.com/watch?v={vid_id}"
            with cols[i % 2]:
                st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration:none;">
                  <div style="border:0.5px solid #e0e0e0; border-radius:12px; overflow:hidden;
                              margin-bottom:12px; background:#fff; transition:box-shadow 0.2s;">
                    <div style="position:relative;">
                      <img src="{thumb}" style="width:100%; display:block;" />
                      <div style="position:absolute;inset:0;display:flex;align-items:center;
                                   justify-content:center;background:rgba(0,0,0,0.25);">
                        <span style="font-size:32px;">▶</span>
                      </div>
                    </div>
                    <div style="padding:10px 12px 12px;">
                      <p style="font-size:12px;color:#888;margin:0 0 4px;">{to_city}</p>
                      <p style="font-size:14px;font-weight:600;color:#111;margin:0;line-height:1.4;">{title}</p>
                      <span style="display:inline-block;margin-top:6px;font-size:11px;padding:2px 8px;
                                    border-radius:4px;background:#e8f0fe;color:#1a73e8;">{label}</span>
                    </div>
                  </div>
                </a>
                """, unsafe_allow_html=True)
                
    with tab4:
        st.subheader("📋 Trip Summary")
        col1, col2,col3 = st.columns(3)
        with col1:
           st.info(f"📍 From: Ahmedabad\n\n🏖 To: {to_city}")
        with col2:
           st.info(f"👨‍👩‍👧 Travelers: {num_travelers}\n\n📅 Days: {num_days}")
        with col3:
           st.info(f"🚘 Transport: {mode}\n\n💰 Budget: {budget}")
    
        st.subheader("💰 Cost breakdown")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.metric("🏨 Hotel" , f" ₹{hotel:,.0f}")
        with col2:
            st.metric("🍕 Food ",f" ₹{food:,.0f}")
        with col3:
            st.metric("🚘 Travel ",f" ₹{travel:,.0f}")
        with col4:
            st.metric("🛍 Shopping ",f"₹ {shopping:,.0f}")
        st.divider()
        gst = inr_budget * 0.18
        total_cost = inr_budget + gst
        st.subheader("💵 Total Estimated Cost")
        col1,col2,col3 = st.columns(3)
        with col1:
            st.metric("Subtotal", f"₹ {inr_budget:,.0f}")
        with col2:
            st.metric("GST (18%)", f"₹ {gst:,.0f}")
        with col3:
            st.metric("Total", f"₹ {total_cost:,.0f}")
        st.success(f"💰 Total Payable Amount : ₹ {total_cost:,.0f}")

        st.divider()
        st.subheader("🎁 Apply Coupon")
        coupon_code = st.text_input("Enter Coupon Code")
        discount = 0
        if coupon_code == "Deepak10":
            discount = total_cost * 0.10
            st.success(f"🎉 Coupon Applied! You saved ₹ {discount:,.0f}")
        final_amount = total_cost - discount
        st.metric("💳 Final Amount to Pay", f"₹ {final_amount:,.0f}")
        st.divider()
        if st.button("📅 Book Now"):
            st.balloons()
            time.sleep(2)
            st.success("🎉 Your trip has been booked successfully!")
            st.session_state.show_budget = False
            st.rerun()
                 

    with tab5:

        col1, col2 = st.columns(2)

        with col1:
            categories = ["Hotel", "Food", "Travel", "Shopping"]
            costs = [hotel, food, travel, shopping]
            st.subheader("📊 Budget Breakdown")

            fig, ax = plt.subplots(figsize=(5, 3))

            fig.patch.set_alpha(0)
            ax.set_facecolor("#111111")

            bars = ax.bar(
                categories,
                costs,
                color=["#FF6B6B", "#4ECDC4", "#45B7D1", "#F9A826"],
                width=0.55
            )

            ax.set_title("Budget Breakdown", color="white", fontsize=12)
            ax.tick_params(colors="white")

            for spine in ax.spines.values():
                spine.set_visible(False)

            ax.grid(axis="y", linestyle="--", alpha=0.2)

            for bar in bars:
                y = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    y,
                    f"₹{y:,.0f}",
                    ha="center",
                    color="white",
                    fontsize=8
                )

            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            st.subheader("🥧 Budget Distribution")

            fig2, ax2 = plt.subplots(figsize=(5, 3))

            fig2.patch.set_alpha(0)
            ax2.set_facecolor("#111111")

            ax2.pie(
                costs,
                labels=categories,
                autopct="%1.1f%%",
                startangle=90,
                colors=["#FF6B6B", "#4ECDC4", "#45B7D1", "#F9A826"],
                explode=[0.03]*4,
                textprops={"color": "white"},
                wedgeprops={"linewidth": 1, "edgecolor": "#222"}
            )

            ax2.set_title("Budget Distribution", color="white")
            plt.tight_layout()

            st.pyplot(fig2)

        st.divider()
        st.subheader("📈 Budget Trend")

        fig3, ax3 = plt.subplots(figsize=(8, 3))

        fig3.patch.set_alpha(0)
        ax3.set_facecolor("#111111")

        ax3.plot(
            categories,
            costs,
            marker="o",
            linewidth=3,
            markersize=8
        )

        ax3.tick_params(colors="white")

        for spine in ax3.spines.values():
            spine.set_visible(False)

        ax3.grid(alpha=0.3, linestyle="--")

        for i, value in enumerate(costs):
            ax3.text(
                i,
                value,
                f"₹{value:,.0f}",
                color="white",
                fontsize=8,
                ha="center"
            )

        ax3.set_title("Budget Trend", color="white")
        plt.tight_layout()

        st.pyplot(fig3)

        st.divider()
        st.subheader("💰 Cost Summary")

        m1, m2, m3, m4 = st.columns(4)

        m1.info(f"🏨 Hotel   ₹{hotel:,.0f}")
        m2.info(f"🍕 Food    ₹{food:,.0f}")
        m3.info(f"🚘 Travel  ₹{travel:,.0f}")
        m4.info(f"🛍 Shopping ₹{shopping:,.0f}")

        # ================= TABLE =================
        st.divider()
        st.subheader("📋 Detailed Breakdown")

        budget_df = pd.DataFrame({
            "Category": ["🏨 Hotel", "🍕 Food", "🚘 Travel", "🛍 Shopping"],
            "Estimated Cost (₹)": [
                round(hotel),
                round(food),
                round(travel),
                round(shopping)
            ]
        })

        st.dataframe(
            budget_df,
            use_container_width=True,
            hide_index=True
        )
    with tab6:
        st.subheader("🗺 Trip Route Map")

        m = folium.Map(location=[to_lat, to_lon],zoom_start=5)
        folium.Marker(
            [from_lat, from_lon],popup="From : Ahmedabad",tooltip="Ahmedabad",icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([to_lat, to_lon],popup=f"Destination : {to_city}",tooltip=to_city,icon=folium.Icon(color="red")).add_to(m)
        route_points = [[from_lat, from_lon],
            [(from_lat + to_lat) / 2, from_lon + 1],[to_lat, to_lon]]
        folium.PolyLine(route_points,color="blue",weight=6,opacity=0.8).add_to(m)
        st_folium(m, width=700, height=500)




