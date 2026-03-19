import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Steam Library Analyst", page_icon="🎮", layout="wide")

API_KEY = st.secrets["STEAM_API_KEY"]
STEAM_ID = st.secrets["STEAM_ID"]

@st.cache_data
def get_steam_library():
    # We added '&include_played_free_games=1' so Gacha/Free games show up!
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAM_ID}&format=json&include_appinfo=1&include_played_free_games=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for errors
        data = response.json()
        games = data['response']['games']
        
        df = pd.DataFrame(games)
        
        # 1. Clean the Data
        df['playtime_hours'] = round(df['playtime_forever'] / 60, 1)
        
        # 2. CREATE THE IMAGE URL COLUMN
        # Steam stores images at this specific URL pattern
        df['image_url'] = df['appid'].apply(lambda x: f"https://steamcdn-a.akamaihd.net/steam/apps/{x}/header.jpg")
        
        return df[['name', 'playtime_hours', 'image_url', 'appid']]
        
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# --- DASHBOARD UI ---
st.title("🎮 My Steam Library Analyst")

with st.spinner("Fetching library..."):
    df = get_steam_library()

if not df.empty:
    # Metrics
    total_hours = df['playtime_hours'].sum()
    fav_game = df.loc[df['playtime_hours'].idxmax()]['name']
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Games Owned", len(df))
    c2.metric("Total Hours", f"{total_hours:,.0f}")
    c3.metric("Favorite Game", fav_game)
    
    st.divider()
    
    # 3. DISPLAY WITH IMAGES
    st.subheader("🏆 Top Games by Playtime")
    
    # Sort and pick Top 15
    top_games = df.sort_values(by='playtime_hours', ascending=False).head(15)

        # Sort by playtime
    top_10 = df.sort_values(by='playtime_hours', ascending=False).head(10)
    
    # Draw the Bar Chart
    st.bar_chart(top_10, x="name", y="playtime_hours", color="#1b2838") 
    
    # We use 'column_config' to tell Streamlit that 'image_url' is actually a Picture
    st.dataframe(
        top_games,
        column_config={
            "image_url": st.column_config.ImageColumn("Cover Art", width="medium"),
            "playtime_hours": st.column_config.NumberColumn("Hours Played", format="%.1f hrs"),
            "name": "Game Title",
            "appid": None # Hide the AppID (it's ugly)
        },
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("No games found! Check your API Key and ID.")