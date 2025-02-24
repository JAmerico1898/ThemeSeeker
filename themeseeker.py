import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import googleapiclient.discovery
import googleapiclient.errors
import google.generativeai as genai
import os
from googleapiclient.discovery import build
import re
from bs4 import BeautifulSoup
import html

# Set page config
st.set_page_config(
    page_title="Spirituality Trends Analyzer",
    page_icon="✨",
    layout="wide"
)

# App title and description
st.title("Spirituality YouTube Trend Analyzer")
st.markdown("""
This application mines popular YouTube videos related to spirituality from different time periods 
and uses Gemini AI to suggest thematic content for lectures targeting various age groups.
""")

# Initialize session state for philosophy context
if 'philosophy_context' not in st.session_state:
    st.session_state['philosophy_context'] = ""

# Sidebar for API keys
with st.sidebar:
    # Hide API Configuration for security
    # Use environment variables or secrets management instead
    youtube_api_key = st.secrets["youtube_api_key"]  # or replace with your API key string
    gemini_api_key = st.secrets["GOOGLE_API_KEY"]
    
    st.header("Search Parameters")
    search_query = st.text_input("Search Query", value="spirituality philosophy meaning of life")
    max_results = st.slider("Maximum Videos per Time Period", 5, 50, 20)
    
    # Instead of file upload, we'll load the HTML content from the provided file
    st.header("Philosophy Context")
    st.info("Philosophy context has been loaded from the Rosacruz Áurea website")
    
    # Process the HTML content that was provided
    try:
        # The HTML content is the one from the document uploaded previously
        content = """
<!DOCTYPE html>
<html class="html" lang="pt-BR">
<head>
    <!-- Head content omitted for brevity -->
</head>
<body class="home page-template-default page page-id-7 wp-embed-responsive oceanwp-theme dropdown-mobile default-breakpoint content-full-screen has-topbar page-header-disabled has-breadcrumbs elementor-default elementor-kit-4 elementor-page elementor-page-7">
    <!-- Body content from the Rosacruz Áurea website -->
    <div class="entry clr" itemprop="text">
        <h3>Rosacruz Áurea | LECTORIUM ROSICRUCIANUM</h3>
        <p>A Rosacruz Áurea é uma Escola iniciática contemporânea, dedicada à transformação da consciência e da vida do ser humano atual.</p>
        <p>A fonte do conhecimento da Rosacruz Áurea é a própria Sabedoria Universal, manifestada em todos os tempos, culturas e povos.</p>
        <p>A Rosacruz Áurea dirige-se ao ser humano buscador, oferecendo-lhe elementos para que ele encontre em si mesmo suas respostas e as converta em seu próprio caminho de transformação. Estes elementos também se encontram em seu símbolo: ponto central, triângulo, quadrado e círculo. Juntos, eles representam em todos os níveis, macrocósmico, cósmico ou microcósmico, um símbolo universal da criação divina.</p>
        <p>A consciência humana é prisioneira de seu próprio egocentrismo. Esse estado de consciência nunca será a base do processo de iniciação. Aqueles que desejam seguir o caminho da iniciação devem superar a si mesmos, pois aqueles que se superam tornam-se capazes de verdadeiramente amar e servir a humanidade e o mundo.</p>
        <p>O Caminho da Iniciação tem diferentes aspectos: 1. Autoconhecimento: tornar-se consciente do seu próprio egocentrismo; 2. Conexão: estabelecer a conexão inicial e consciente com o Ser Real e superar o egocentrismo; 3. Nova Consciência: através dessa conexão inicial, transformar o pensamento, o sentimento e a ação, permitindo o surgimento de uma nova consciência;</p>
        <p>4. Consciência Espiritual: por meio de um trabalho contínuo, a nova consciência se desenvolve e amadurece, unindo-se plenamente ao Ser Real; 5. Transmutação: a consciência espiritual desencadeia uma transformação energética dos veículos da personalidade, focando em seus aspectos mais sutis; 6. Nova Vitalidade: a transformação energética caminha para uma transformação orgânica, resultando em uma nova e total energia vital;</p>
        <p>7. Reintegração: reintegrado ao universo, o novo ser humano torna-se um servo do mundo e da humanidade. </p>
    </div>
</body>
</html>
        """
        
        # Store the raw HTML content
        st.session_state['philosophy_context'] = content
        
        # Extract text from HTML using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        cleaned_text = soup.get_text()
        
        # Clean up the text
        lines = (line.strip() for line in cleaned_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Store cleaned text
        st.session_state['philosophy_context_cleaned'] = cleaned_text
        
        # Show a sample of the extracted text
        with st.expander("Preview extracted text"):
            st.write(cleaned_text[:2700] + "..." if len(cleaned_text) > 2700 else cleaned_text)
            
    except Exception as e:
        st.error(f"Error processing philosophy context: {str(e)}")
        
    st.caption("Note: This application requires API keys to function properly.")

# Function to get date in ISO format for a given period
def get_date_for_period(period):
    today = datetime.now()
    
    if period == "1 week":
        past_date = today - timedelta(weeks=1)
    elif period == "1 month":
        past_date = today - timedelta(days=30)
    elif period == "6 months":
        past_date = today - timedelta(days=180)
    else:
        return None
        
    return past_date.strftime("%Y-%m-%dT%H:%M:%SZ")

# Function to get popular videos from YouTube
def get_popular_videos(api_key, query, max_results, published_after):
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        
        # First get video IDs from search
        search_request = youtube.search().list(
            part="id,snippet",
            q=query,
            type="video",
            order="viewCount",
            publishedAfter=published_after,
            maxResults=max_results
        )
        search_response = search_request.execute()
        
        # Extract video IDs
        video_ids = [item['id']['videoId'] for item in search_response['items']]
        
        # Get detailed video statistics
        videos_request = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids)
        )
        videos_response = videos_request.execute()
        
        # Process and return the results
        results = []
        for item in videos_response['items']:
            results.append({
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'published_at': item['snippet']['publishedAt'],
                'view_count': int(item['statistics'].get('viewCount', 0)),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'video_id': item['id'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'description': item['snippet']['description']
            })
        
        # Sort by view count
        results.sort(key=lambda x: x['view_count'], reverse=True)
        return results
    
    except Exception as e:
        st.error(f"Error fetching YouTube data: {str(e)}")
        return []

# Function to generate brief context for each video
def generate_video_context(title, description):
    # Extract first 200 characters of description or less
    brief_desc = description[:200] + "..." if len(description) > 200 else description
    
    # Simple rule-based contextualizing (could be replaced with more sophisticated NLP)
    context = ""
    
    if re.search(r'meditation|mindfulness', title.lower() + brief_desc.lower()):
        context = "Meditation/Mindfulness practice"
    elif re.search(r'buddhis|zen|tao', title.lower() + brief_desc.lower()):
        context = "Eastern philosophy"
    elif re.search(r'christian|jesus|bible|faith', title.lower() + brief_desc.lower()):
        context = "Christian spirituality"
    elif re.search(r'islam|muslim|quran', title.lower() + brief_desc.lower()):
        context = "Islamic spirituality"
    elif re.search(r'judaism|jewish|torah', title.lower() + brief_desc.lower()):
        context = "Jewish spirituality"
    elif re.search(r'hindu|vedanta|yoga', title.lower() + brief_desc.lower()):
        context = "Hindu spirituality"
    elif re.search(r'consciousness|awareness', title.lower() + brief_desc.lower()):
        context = "Consciousness exploration"
    elif re.search(r'psychedelic|plant medicine|ayahuasca|dmt', title.lower() + brief_desc.lower()):
        context = "Psychedelic spirituality"
    elif re.search(r'near death|afterlife|heaven', title.lower() + brief_desc.lower()):
        context = "Afterlife exploration"
    elif re.search(r'science|physics|quantum', title.lower() + brief_desc.lower()):
        context = "Science and spirituality"
    elif re.search(r'gnosticism|gnostic|consciousness|awareness', title.lower() + brief_desc.lower()):
        context = "Gnosticism"
    else:
        context = "General spiritual content"
    
    return context

# Function to use Gemini to generate lecture themes
def generate_lecture_themes(api_key, video_data, age_group):
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare prompt with video titles and contexts
        titles_context = "\n".join([f"- {video['title']} ({video['context']})" for video in video_data])
        
        # Define age group characteristics
        age_characteristics = {
            "20-30": "digital natives, social media focused, seeking authenticity, concerned about climate crisis, mental health aware",
            "30-40": "career-focused, starting families, balancing work-life, health conscious, pragmatic spirituality",
            "40-50": "mid-life reflection, established careers, parenting teens, seeking deeper meaning, stress management",
            "50-60": "empty nest transitions, career peak or change, caring for aging parents, legacy considerations",
            "60+": "retirement planning/living, health challenges, grandparenting, mortality awareness, wisdom sharing"
        }
        
        # Get philosophical context if available
        philosophy_context = ""
        if 'philosophy_context_cleaned' in st.session_state and st.session_state['philosophy_context_cleaned']:
            full_context = st.session_state['philosophy_context_cleaned']
            # Limit context length to avoid token limits
            if len(full_context) > 10000:
                philosophy_context = full_context[:10000] + "..."
            else:
                philosophy_context = full_context
        
        # Add philosophy context to the prompt if available
        if philosophy_context:
            prompt = f"""
As a spiritual content creator for a philosophical school of thought, analyze these trending YouTube video titles related to spirituality:

{titles_context}

The philosophical school has the following context, which should guide your suggestions:
----
{philosophy_context}
----

Based on these trends and the philosophical context, suggest 10 compelling lecture themes that would resonate specifically with people aged {age_group} years. 
Consider that this age group typically has these characteristics: {age_characteristics.get(age_group, "")}.

Make sure your suggested themes align with the philosophical approach described in the context.

For each theme:
1. Provide a catchy title that reflects both current trends and the philosophical approach
2. Write a short description (2-3 sentences)
3. Explain why this theme would resonate with this specific age group
4. Briefly note how it connects to the philosophical context
5. Outline a 30-minute lecture based on the theme.

Format your response as a numbered list with the title in bold, followed by the description and reasoning.
"""
        else:
            # Original prompt without philosophical context
            prompt = f"""
As a spiritual content creator, analyze these trending YouTube video titles related to spirituality:

{titles_context}

Based on these trends, suggest 5 compelling lecture themes that would resonate specifically with people aged {age_group} years. 
Consider that this age group typically has these characteristics: {age_characteristics.get(age_group, "")}.

For each theme:
1. Provide a catchy title that reflects both current trends and the philosophical approach
2. Write a short description (2-3 sentences)
3. Explain why this theme would resonate with this specific age group
4. Briefly note how it connects to the philosophical context
5. Outline a 30-minute lecture based on the theme.


Format your response as a numbered list with the title in bold, followed by the description and reasoning.
"""

        # Generate the response
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error generating lecture themes: {str(e)}"

# Main app layout
tab1, tab2, tab3 = st.tabs(["Mine YouTube Videos", "Lecture Theme Generator", "About"])

with tab1:
    st.header("Mine Popular Spirituality Videos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Last Week")
        if st.button("Mine Last Week's Videos"):
            if youtube_api_key:
                with st.spinner("Fetching last week's popular videos..."):
                    published_after = get_date_for_period("1 week")
                    videos = get_popular_videos(youtube_api_key, search_query, max_results, published_after)
                    
                    if videos:
                        # Add context to each video
                        for video in videos:
                            video['context'] = generate_video_context(video['title'], video['description'])
                        
                        # Store in session state for later use
                        st.session_state['weekly_videos'] = videos
                        
                        # Display videos
                        for i, video in enumerate(videos):
                            st.write(f"**{i+1}. {video['title']}**")
                            st.write(f"*Context: {video['context']}*")
                            st.write(f"Views: {video['view_count']:,} | Channel: {video['channel']}")
                            st.write(f"[Watch on YouTube](https://www.youtube.com/watch?v={video['video_id']})")
                            st.image(video['thumbnail'], use_container_width=True)
                            st.divider()
                    else:
                        st.warning("No videos found or error occurred.")
            else:
                st.error("Please enter your YouTube API key in the sidebar.")
    
    with col2:
        st.subheader("Last Month")
        if st.button("Mine Last Month's Videos"):
            if youtube_api_key:
                with st.spinner("Fetching last month's popular videos..."):
                    published_after = get_date_for_period("1 month")
                    videos = get_popular_videos(youtube_api_key, search_query, max_results, published_after)
                    
                    if videos:
                        # Add context to each video
                        for video in videos:
                            video['context'] = generate_video_context(video['title'], video['description'])
                        
                        # Store in session state for later use
                        st.session_state['monthly_videos'] = videos
                        
                        # Display videos
                        for i, video in enumerate(videos):
                            st.write(f"**{i+1}. {video['title']}**")
                            st.write(f"*Context: {video['context']}*")
                            st.write(f"Views: {video['view_count']:,} | Channel: {video['channel']}")
                            st.write(f"[Watch on YouTube](https://www.youtube.com/watch?v={video['video_id']})")
                            st.image(video['thumbnail'], use_container_width=True)
                            st.divider()
                    else:
                        st.warning("No videos found or error occurred.")
            else:
                st.error("Please enter your YouTube API key in the sidebar.")
    
    with col3:
        st.subheader("Last 6 Months")
        if st.button("Mine Last 6 Months' Videos"):
            if youtube_api_key:
                with st.spinner("Fetching last 6 months' popular videos..."):
                    published_after = get_date_for_period("6 months")
                    videos = get_popular_videos(youtube_api_key, search_query, max_results, published_after)
                    
                    if videos:
                        # Add context to each video
                        for video in videos:
                            video['context'] = generate_video_context(video['title'], video['description'])
                        
                        # Store in session state for later use
                        st.session_state['biannual_videos'] = videos
                        
                        # Display videos
                        for i, video in enumerate(videos):
                            st.write(f"**{i+1}. {video['title']}**")
                            st.write(f"*Context: {video['context']}*")
                            st.write(f"Views: {video['view_count']:,} | Channel: {video['channel']}")
                            st.write(f"[Watch on YouTube](https://www.youtube.com/watch?v={video['video_id']})")
                            st.image(video['thumbnail'], use_container_width=True)
                            st.divider()
                    else:
                        st.warning("No videos found or error occurred.")
            else:
                st.error("Please enter your YouTube API key in the sidebar.")

with tab2:
    st.header("Generate Lecture Themes by Age Group")
    
    # Show philosophy context status
    if 'philosophy_context_cleaned' in st.session_state and st.session_state['philosophy_context_cleaned']:
        context_length = len(st.session_state['philosophy_context_cleaned'])
        st.success(f"✅ Philosophy context loaded ({context_length} characters)")
        with st.expander("View loaded philosophical context"):
            st.write(st.session_state['philosophy_context_cleaned'][:2700] + "..." 
                    if context_length > 2700 else st.session_state['philosophy_context_cleaned'])
    else:
        st.warning("⚠️ No philosophical context loaded. Upload an HTML file in the sidebar to provide context.")
    
    # Select data source
    data_source = st.selectbox(
        "Select Video Data Source",
        ["Last Week", "Last Month", "Last 6 Months", "Combined (All Time Periods)"]
    )
    
    # Map selection to session state keys
    data_mapping = {
        "Last Week": 'weekly_videos',
        "Last Month": 'monthly_videos',
        "Last 6 Months": 'biannual_videos'
    }
    
    # Get videos from selected source
    selected_videos = []
    if data_source in data_mapping:
        selected_videos = st.session_state.get(data_mapping[data_source], [])
    elif data_source == "Combined (All Time Periods)":
        # Combine all video sources
        weekly = st.session_state.get('weekly_videos', [])
        monthly = st.session_state.get('monthly_videos', [])
        biannual = st.session_state.get('biannual_videos', [])
        
        # Add source field to track which time period each video came from
        for v in weekly:
            v['source'] = 'Last Week'
        for v in monthly:
            v['source'] = 'Last Month'
        for v in biannual:
            v['source'] = 'Last 6 Months'
        
        # Combine and deduplicate by video ID
        all_videos = weekly + monthly + biannual
        video_ids_seen = set()
        selected_videos = []
        
        for video in all_videos:
            if video['video_id'] not in video_ids_seen:
                selected_videos.append(video)
                video_ids_seen.add(video['video_id'])
    
    # Show summary of available videos
    if selected_videos:
        st.write(f"Found {len(selected_videos)} videos from {data_source}")
        
        # Display a sample of video titles (first 5)
        st.write("Sample of video titles:")
        for i, video in enumerate(selected_videos[:5]):
            st.write(f"{i+1}. {video['title']} - *{video['context']}*")
        
        if len(selected_videos) > 5:
            st.write(f"...and {len(selected_videos)-5} more")
    else:
        st.warning(f"No videos available for {data_source}. Please mine videos in the first tab.")
    
    # Age group selection
    age_group = st.selectbox(
        "Select Target Age Group",
        ["20-30", "30-40", "40-50", "50-60", "60+"]
    )
    
    # Generate themes button
    if st.button("Generate Lecture Themes"):
        if gemini_api_key and selected_videos:
            with st.spinner(f"Generating lecture themes for {age_group} age group..."):
                themes = generate_lecture_themes(gemini_api_key, selected_videos, age_group)
                st.markdown(themes)
        elif not gemini_api_key:
            st.error("Please enter your Google Gemini API key in the sidebar.")
        else:
            st.error("No video data available. Please mine videos first.")

with tab3:
    st.header("About This Application")
    st.markdown("""
    ### Purpose
    This application is designed to help philosophical and spiritual educators identify trending topics 
    and create age-appropriate lecture content based on current interests in spirituality.
    
    ### How It Works
    1. **Data Mining**: The app connects to YouTube's API to find the most viewed videos on spirituality 
       from three different time periods.
    
    2. **Content Analysis**: Each video is briefly contextualized to identify its spiritual domain or approach.
    
    3. **Theme Generation**: Google's Gemini AI analyzes the trending content and suggests lecture themes 
       tailored to different generational perspectives and needs.
    
    ### Requirements
    - YouTube Data API v3 key (get one from [Google Cloud Console](https://console.cloud.google.com/))
    - Google Gemini API key
    
    ### Privacy
    This application does not store any data outside your browser session. API keys are not saved 
    between sessions for security reasons.
    """)

# Footer
st.divider()
st.caption("© 2025 Spirituality Trends Analyzer | Developed for philosophical education")