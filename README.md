# Spirituality YouTube Trend Analyzer

A Streamlit application that empowers philosophical and spiritual educators to identify trending spirituality topics on YouTube and generate age-appropriate lecture content and documents in both English and Portuguese, based on current interest and philosophical alignment.

---

## ✨ Features

- **YouTube Mining**: Connects to YouTube's API to find the most-viewed spirituality-related videos across three timeframes: 1 week, 1 month, and 6 months.
- **Content Categorization**: Automatically classifies videos into spiritual domains like mindfulness, religious traditions, consciousness, and more.
- **Philosophical Context**: Integrates teachings from *Rosacruz Áurea* to ensure content alignment with its spiritual worldview.
- **Theme Generation**: Uses Google's Gemini AI to propose lecture themes that resonate with different age groups and current video trends.
- **Age-Specific Insights**: Suggests tailored themes for various demographics (20-30, 30-40, 40-50, 50-60, 60+).
- **Multilingual Support**: Automatically translates generated themes into **Portuguese**.
- **Document Generation**: Generates professional Word documents (in English or Portuguese) for selected themes, with images and formatted content ready to print or share.

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher  
- YouTube Data API key  
- Google Gemini API key

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/spirituality-youtube-analyzer.git
   cd spirituality-youtube-analyzer
   ```

2. Create and activate a virtual environment:

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API keys as environment variables:

   **Windows:**
   ```cmd
   set YOUTUBE_API_KEY=your_youtube_api_key
   set GEMINI_API_KEY=your_gemini_api_key
   ```

   **macOS/Linux:**
   ```bash
   export YOUTUBE_API_KEY=your_youtube_api_key
   export GEMINI_API_KEY=your_gemini_api_key
   ```

---

## 🚀 Usage

Start the app:

```bash
streamlit run themeseeker.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📚 How It Works

1. **Search YouTube Trends**  
   Set your search terms and time window (last week, month, or 6 months). The app fetches and ranks videos by view count.

2. **Analyze & Categorize**  
   Videos are automatically tagged into spiritual categories using heuristics and NLP.

3. **Generate Lecture Themes**  
   Select your desired age group and let Gemini AI generate lecture themes. All themes are aligned with the Rosacruz Áurea philosophical context.

4. **Translate to Portuguese**  
   Themes are automatically translated into natural, idiomatic Portuguese for Brazilian or Portuguese-speaking audiences.

5. **Export Professional Documents**  
   Generate `.docx` documents with title, teaser, 500-word explanation, and a themed image — ready to distribute as lecture materials.

---

## ⏳ API Usage Notes

- **YouTube Data API**: Free daily quota of 10,000 units. Each search request ~100 units.
- **Google Gemini API**: Pricing based on input/output tokens. Visit [Google Cloud pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) for details.

---

## 🤝 Contributing

Contributions are welcome! Fork the repository, create a new branch, and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Rosacruz Áurea](https://www.rosacruzaurea.org.br/) for philosophical inspiration  
- [YouTube Data API](https://developers.google.com/youtube/v3)  
- [Google Gemini AI](https://ai.google.dev/gemini-api)  
- [Streamlit](https://streamlit.io) for the interactive app framework  
- [Unsplash](https://unsplash.com/) for thematic images  
