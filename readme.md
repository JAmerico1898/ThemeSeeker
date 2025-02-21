# Spirituality YouTube Trend Analyzer

A Streamlit application that helps philosophical and spiritual educators identify trending topics on YouTube and generate age-appropriate lecture content based on current interests in spirituality.

![Spirituality YouTube Trend Analyzer](https://i.imgur.com/placeholder.jpg)

## Features

- **YouTube Mining**: Connect to YouTube's API to find the most-viewed videos on spirituality from three different time periods (1 week, 1 month, 6 months)
- **Content Analysis**: Each video is automatically categorized and contextualized to identify its spiritual domain or approach
- **Philosophical Context**: Incorporates the philosophy of Rosacruz Áurea to ensure generated content aligns with the school's approach
- **Theme Generation**: Leverages Google's Gemini AI to analyze trending content and suggest lecture themes
- **Age-Specific Content**: Tailors lecture suggestions to different age groups (20-30, 30-40, 40-50, 50-60, 60+)

## Installation

### Prerequisites

- Python 3.8 or higher
- A YouTube Data API key
- A Google Gemini API key

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/spirituality-youtube-analyzer.git
   cd spirituality-youtube-analyzer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API keys as environment variables:
   
   **On Windows:**
   ```
   set YOUTUBE_API_KEY=your_youtube_api_key_here
   set GEMINI_API_KEY=your_gemini_api_key_here
   ```
   
   **On macOS/Linux:**
   ```
   export YOUTUBE_API_KEY=your_youtube_api_key_here
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run app.py
   ```

2. Access the web interface at `http://localhost:8501`

3. Set your search parameters in the sidebar

4. Mine trending spirituality videos from your desired time periods

5. Generate lecture themes by selecting:
   - A data source (Last Week, Last Month, Last 6 Months, or Combined)
   - A target age group (20-30, 30-40, 40-50, 50-60, 60+)

## How It Works

### YouTube Mining Process

The application uses the YouTube Data API to search for videos based on spirituality-related keywords, then orders them by view count within the specified time period. For each video, it retrieves:

- Title and description
- View count, likes, and comments
- Channel information
- Thumbnail images

### Content Categorization

Videos are automatically categorized into spiritual contexts such as:
- Meditation/Mindfulness
- Eastern philosophy
- Various religious traditions
- Consciousness exploration
- Science and spirituality
- General spiritual content

### Lecture Theme Generation

The Gemini AI model processes:
1. Trending video titles and their contexts
2. The philosophical approach of Rosacruz Áurea
3. Characteristics of the selected age group

It then generates lecture themes that:
- Resonate with current interests
- Align with the philosophical approach
- Address the specific needs and perspectives of the target age group

## API Quotas and Limits

- YouTube Data API has a free daily quota of 10,000 units. Each search request uses approximately 100 units.
- Google Gemini API has pricing based on input and output tokens. Check the current pricing on Google's website.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Rosacruz Áurea for their philosophical context
- YouTube Data API
- Google Gemini AI
- Streamlit framework

---

*This tool was developed to support spiritual educators in creating relevant, timely content that meets the needs of modern spiritual seekers.*
