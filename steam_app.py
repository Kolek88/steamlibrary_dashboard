import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Steam Library Analyst", layout="wide")

API_KEY = st.secrets["STEAM_API_KEY"]
STEAM_ID = st.secrets["STEAM_ID"]

@st.cache_data
def get_steam_library():
    # API URL includes free-to-play games
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAM_ID}&format=json&include_appinfo=1&include_played_free_games=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        games = data['response']['games']
        
        df = pd.DataFrame(games)
        
        # Convert playtime from minutes to hours
        df['playtime_hours'] = round(df['playtime_forever'] / 60, 1)
        
        # Generate Steam CDN image URLs
        df['image_url'] = df['appid'].apply(lambda x: f"https://steamcdn-a.akamaihd.net/steam/apps/{x}/header.jpg")
        
        return df[['name', 'playtime_hours', 'image_url', 'appid']]
        
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# Dashboard UI
st.title("My Steam Library Analyst")

with st.spinner("Fetching library..."):
    df = get_steam_library()

if not df.empty:
    # Calculate summary metrics
    total_hours = df['playtime_hours'].sum()
    fav_game = df.loc[df['playtime_hours'].idxmax()]['name']
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Games Owned", len(df))
    c2.metric("Total Hours", f"{total_hours:,.0f}")
    c3.metric("Favorite Game", fav_game)
    
    st.divider()
    
    st.subheader("Top Games by Playtime")
    
    # Filter datasets for visualizations
    top_games = df.sort_values(by='playtime_hours', ascending=False).head(15)
    top_10 = df.sort_values(by='playtime_hours', ascending=False).head(10)
    
    st.bar_chart(top_10, x="name", y="playtime_hours", color="#1b2838") 
    
    # Render dataframe with image columns
    st.dataframe(
        top_games,
        column_config={
            "image_url": st.column_config.ImageColumn("Cover Art", width="medium"),
            "playtime_hours": st.column_config.NumberColumn("Hours Played", format="%.1f hrs"),
            "name": "Game Title",
            "appid": None 
        },
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("No games found. Verify API Key and Steam ID.")