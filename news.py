import streamlit as st
import requests

# Set up the Streamlit app
st.set_page_config(page_title="Indian Stock Market News", layout="centered")

# Custom CSS for styling (hide sidebar)
st.markdown(
    """
    <style>
    /* Hide the sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }
    /* Remove max-width and center content */
    .stApp {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 20px;
    }
    /* Black navbar */
    .navbar {
        background-color: black;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        width: 100%;
    }
    .navbar a {
        color: white;
        margin: 0 15px;
        text-decoration: none;
        font-weight: bold;
    }
    .navbar a:hover {
        color: skyblue;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to fetch Indian stock market news
def get_news():
    try:
        # Use NewsAPI or any other news API (replace with your API key)
        api_key = "3a7281c617d048f8ad9468e6516c017e"  # Replace with your actual API key
        url = f"https://newsapi.org/v2/everything?q=Indian stock market&apiKey={api_key}&pageSize=10"  # Limit to 10 articles
        response = requests.get(url)
        if response.status_code == 200:
            news_data = response.json()
            return news_data.get("articles", [])
        else:
            return []
    except Exception as e:
        return []

# Black Navbar
st.markdown(
    """
    <div class="navbar">
        <a href="/">Home</a>
        <a href="/search">Search</a>
        <a href="/news">News</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Title and header
st.title("📰 Indian Stock Market News")

# Fetch and display news
news_articles = get_news()
for article in news_articles[:10]:  # Limit to 10 articles
    st.write(f"#### {article['title']}")
    st.write(f"**Source:** {article['source']['name']}")
    st.write(f"**Published At:** {article['publishedAt']}")
    st.write(f"{article['description']}")
    st.write(f"[Read more]({article['url']})")
    st.write("---")