import streamlit as st
import sqlite3
from datetime import datetime
import hashlib

# Database setup
conn = sqlite3.connect('news_articles.db', check_same_thread=False)
c = conn.cursor()

# Simple user authentication (for demo purposes)
users = {
    "user1": "password1",
    "user2": "password2"
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

hashed_users = {user: hash_password(pw) for user, pw in users.items()}

def login(username, password):
    if username in hashed_users and hash_password(password) == hashed_users[username]:
        return True
    return False

def search_articles(query):
    if query.strip() == "":
        # Return all articles when no search term is provided
        c.execute('''
            SELECT title, author, source, content, date_created, date_updated, mp_mentioned, categories, summary
            FROM articles
            ORDER BY date_created DESC
        ''')
    else:
        query = f"%{query}%"
        c.execute('''
            SELECT title, author, source, content, date_created, date_updated, mp_mentioned, categories, summary
            FROM articles
            WHERE mp_mentioned LIKE ?
            ORDER BY date_created DESC
        ''', (query,))
    return c.fetchall()

# Dialog for article details
@st.dialog("Article Details", width="large")
def show_article_dialog(article):
    st.markdown(f"### {article['title']}")
    st.write(f"**Summary by GENAI:** {article['summary'] if article['summary'] else 'No summary available'}")
    st.write(f"**Author:** {article['author']}")
    st.write(f"**Source:** {article['source']}")
    st.write(f"**Date Created:** {article['date_created']}")
    st.write(f"**Date Updated:** {article['date_updated']}")
    st.write(f"**Categories:** {article['categories'] if article['categories'] else 'No categories'}")
    st.write(f"**MP Mentioned:** {article['mp_mentioned']}")
    st.markdown("---")
    st.markdown(f"<div style='white-space: pre-wrap; max-height: 60vh; overflow-y: auto;'>{article['content']}</div>", unsafe_allow_html=True)

def show_search_page():
    """Main search functionality page"""
    st.title("Press Clipping")
    st.subheader("Search News Articles")
    
    # Create columns for inline search box and button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input("Enter search term (MP mentioned)", label_visibility="collapsed", placeholder="Enter search term (MP mentioned)")
    
    with col2:
        search_button = st.button("Search", use_container_width=True)

    # Perform search when button is clicked
    if search_button:
        st.session_state.search_results = search_articles(search_query)
        st.session_state.search_performed = True

    # Display search results
    if st.session_state.search_performed:
        if st.session_state.search_results:
            if search_query.strip() == "":
                st.info(f"Showing all articles ({len(st.session_state.search_results)} results)")
            else:
                st.info(f"Found {len(st.session_state.search_results)} articles matching '{search_query}'")
            
            cols = st.columns(3)
            for idx, result in enumerate(st.session_state.search_results):
                title, author, source, content, date_created, date_updated, mp_mentioned, categories, summary = result
                col = cols[idx % 3]
                with col:
                    card_key = f"view_article_{idx}"
                    if st.button(
                        f"📰 **{title}**\n\nMP(s): {mp_mentioned if mp_mentioned else 'None'}",
                        key=card_key,
                        help=f"Source: {source}\nClick to view full article",
                        use_container_width=True
                    ):
                        article_data = {
                            "title": title,
                            "author": author,
                            "source": source,
                            "content": content,
                            "date_created": date_created,
                            "date_updated": date_updated,
                            "mp_mentioned": mp_mentioned,
                            "categories": categories,
                            "summary": summary
                        }
                        show_article_dialog(article_data)
        else:
            if search_query.strip() == "":
                st.info("No articles found in the database.")
            else:
                st.info(f"No articles found matching '{search_query}'.")
    else:
        st.info("Welcome! Click Search to view all articles, or enter a search term to filter results.")

def show_about_us():
    """About Us page"""
    st.title("About Us")
    
    st.markdown("""
    ## Transforming Press Clipping Operations
    
    Press Clipping is an innovative automated solution designed to revolutionize how parliamentary library staff monitor and deliver news coverage to Members of Parliament and Ministers.
    
    ### The Challenge We Address
    
    Library staff have traditionally invested considerable time manually searching through numerous news sources to identify articles featuring Members of Parliament. This labor-intensive process involves:
    
    - **Time-Consuming Manual Search**: Staff spend hours daily searching across multiple news platforms
    - **Resource-Intensive Compilation**: Manually collating articles into structured reports for MP review
    - **Delayed Information Delivery**: The manual process often results in delays in providing timely updates
    - **Inconsistent Coverage**: Risk of missing relevant articles due to the volume of daily news content
    - **Reduced Productivity**: Valuable staff time diverted from other critical library services
    
    ### Our Solution
    
    Our automated press clipping system transforms this workflow by leveraging cutting-edge technology to deliver comprehensive, timely, and accurate news monitoring services. We've designed a solution that not only addresses current inefficiencies but anticipates future needs of parliamentary information services.
    
    ### Comprehensive Data Sources
    
    Our system continuously monitors a carefully curated selection of Singapore's most trusted news sources, including:
    
    - **Channel NewsAsia (CNA)** - Singapore's premier news network
    - **The Straits Times** - Singapore's flagship English-language daily
    - **Additional Reliable Sources** - Expanding network of credible local and regional news outlets
    
    We maintain strict editorial standards in our source selection, ensuring all monitored publications meet high journalistic standards and provide accurate, timely reporting.
    
    ### Advanced Application Features
    
    #### 🔍 **Press Clippings Collector**
    Our intelligent crawling system operates continuously, automatically identifying and collecting relevant articles from monitored news sources. This ensures comprehensive coverage without the risk of human oversight.
    
    #### 🤖 **AI-Powered Summariser**
    Leveraging state-of-the-art Large Language Models (LLMs), our system provides:
    - **Intelligent Summaries**: Concise, accurate summaries of article content
    - **Automatic Categorization**: Smart classification of articles by topic (Finance, Environment, Healthcare, etc.)
    - **MP Recognition**: Automated extraction and identification of mentioned Members of Parliament
    - **Enhanced Value**: Additional analytical insights for VVIPs, Ministers, and MPs
    
    #### 📊 **Comprehensive Research Tool**
    Our search and retrieval system empowers library staff with:
    - **Instant Access**: Rapid retrieval of all press clippings related to specific MPs
    - **Structured Presentation**: Professional formatting with title, date, source, and content
    - **Advanced Filtering**: Multiple search parameters for precise results
    - **Export Capabilities**: Easy compilation for MP briefings and reports
    
    ### Impact and Benefits
    
    #### For Library Staff:
    - **Dramatic Time Savings**: Reduction from hours to minutes for press clipping preparation
    - **Enhanced Accuracy**: Automated systems reduce risk of missed articles
    - **Improved Focus**: Staff can concentrate on higher-value analytical tasks
    - **Consistent Quality**: Standardized formatting and presentation
    
    #### For MPs and Ministers:
    - **Timely Information**: Faster delivery of relevant news coverage
    - **Comprehensive Coverage**: No missed articles due to manual oversight
    - **Enhanced Insights**: AI-powered summaries and categorization
    - **Professional Presentation**: Clean, organized information delivery
    
    """)
    
    st.markdown("---")
    st.markdown("*Last updated: " + datetime.now().strftime("%B %Y") + "*")

def show_methodology():
    """Methodology page"""
    st.title("Methodology")
    
    st.markdown("""
    Our application incorporates automated data retrieval, summarization, and categorization of news articles related to MPs, leveraging OpenAI's GPT-4.1 model to deliver comprehensive and intelligent press clipping services.
    
    ### 1. System Overview
    
    The application consists of two primary features: **Press Clippings Researcher** and **Press Clipping Summarizer**. The system retrieves news articles related to specific MPs, summarizes the content of these articles, and classifies them into predefined categories to assist in presenting relevant information effectively.
    
    #### Data Flow Overview
    
    The data flow is structured into two key stages:
    - **Data Retrieval**: Fetching articles from publicly accessible news sources
    - **Data Processing and Summarization**: Processing, summarizing, and classifying the articles
    
    ### 2. Feature 1: Press Clippings Researcher
    
    This feature enables library staff to quickly retrieve all press clippings related to a particular MP through intelligent search across multiple news sources and efficient data retrieval.
    
    #### Process Steps:
    
    **1. Data Retrieval**
    - A web scraper Python script periodically crawls Singapore news sites for all articles related to Singapore Parliament
    - Automated collection ensures comprehensive coverage without manual intervention
    
    **2. Search Input**
    - Library staff enter the MP's name or specific keywords related to the MP into the application
    - A request is triggered for the system to search monitored news sources (e.g., The Straits Times, CNA)
    - Real-time query processing for immediate results
    
    **3. Search Results Display**
    - The application returns a comprehensive list of articles matching the search query
    - Each article displays essential information: title, date, content, and source link
    - Results are organized chronologically for easy navigation
    
    **4. Data Storage**
    - Retrieved articles are stored in a SQLite database for easy access and retrieval
    - Metadata including article title, publication date, MP names mentioned, and URL are stored for enhanced categorization and future reference
    - Efficient indexing ensures rapid search performance
    
    ### 3. Feature 2: Press Clipping Summarizer
    
    This feature leverages GPT-4.1 to summarize retrieved articles and classify them into categories, enhancing the presentation of press clippings by providing concise summaries and relevant categories for MPs and VVIPs (e.g., Ministers).
    
    #### Process Steps:
    
    **1. AI-Powered Summarization**
    - The LLM processes each article and generates a brief, structured summary capturing essential points relevant to the MP
    - The LLM automatically extracts and identifies MP names mentioned in the content
    - Summaries maintain accuracy while providing concise, actionable insights
    
    **2. Intelligent Article Categorization**
    - The LLM classifies articles into predefined categories based on content analysis (e.g., Finance, Environment, Politics, Healthcare)
    - This categorization enables structured presentation, allowing MPs to quickly identify relevant topics
    - Dynamic categorization adapts to emerging policy areas and current events
    
    **3. Comprehensive Storage**
    - Summarized content and categories are permanently stored in the system for future reference
    
    ### 4. Technical Implementation Details
    
    #### System Architecture
    - **Web Application**: Streamlit serves as both frontend and backend, providing an intuitive user interface
    - **News Sources Crawler**: Custom Python script utilizing BeautifulSoup for efficient article collection from CNA and The Straits Times
    - **LLM Integration**: Summarization and categorization tasks are performed using OpenAI's GPT-4.1 model for superior accuracy
    - **Database Management**: SQLite3 database stores articles, summaries, and categories, ensuring quick retrieval and data persistence
    
    #### Key Technologies
    - **Python**: Core programming language for all system components
    - **Streamlit**: Modern web framework for rapid application development
    - **BeautifulSoup**: Web scraping library for reliable data extraction
    - **OpenAI GPT-4.1**: Advanced language model for summarization and categorization
    - **SQLite3**: Lightweight, efficient database for local data storage
    
    ### 5. Challenges and Considerations
                
    - **Data Accuracy:** Ensuring that the search results are highly relevant and that the LLM summaries are concise and accurate
    - **News Source Access:** Accessing diverse, up-to-date, and reliable news sources can sometimes be a challenge due to rate limits or website restrictions
    - **Scalability:** As the volume of articles increases, the system must scale efficiently, particularly the data retrieval and LLM summarization components
    - **Real-time Processing:** Implementing real-time or near-real-time processing to ensure that MPs receive up-to-date press clippings
                
    ### 6. Flow Chart
    """)
    st.image("./flowchart.png", caption="Press Clip Flowchart")
    
    st.markdown("---")
    st.markdown("*Methodology last updated: " + datetime.now().strftime("%B %Y") + "*")

def main():
    # Configure page
    st.set_page_config(
        page_title="Press Clipping",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state variables
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Search"

    # Login check
    if not st.session_state.logged_in:
        # Center the title
        st.markdown("<h1 style='text-align: center;'>Press Clipping</h1>", unsafe_allow_html=True)
        
        # Center the login form with max width
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                if login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.info("Please log in to access the app.")
        return

    # Sidebar navigation
    with st.sidebar:
        st.title("📰 Press Clipping")
        st.markdown(f"Welcome, {st.session_state.username}")
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🔍 Search", use_container_width=True, type="primary" if st.session_state.current_page == "Search" else "secondary"):
            st.session_state.current_page = "Search"
            st.rerun()
        
        if st.button("ℹ️ About Us", use_container_width=True, type="primary" if st.session_state.current_page == "About Us" else "secondary"):
            st.session_state.current_page = "About Us"
            st.rerun()
        
        if st.button("📋 Methodology", use_container_width=True, type="primary" if st.session_state.current_page == "Methodology" else "secondary"):
            st.session_state.current_page = "Methodology"
            st.rerun()
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.current_page = "Search"
            st.session_state.search_results = []
            st.session_state.search_performed = False
            st.rerun()        

    # Display the selected page
    if st.session_state.current_page == "Search":
        show_search_page()
    elif st.session_state.current_page == "About Us":
        show_about_us()
    elif st.session_state.current_page == "Methodology":
        show_methodology()

if __name__ == "__main__":
    main()