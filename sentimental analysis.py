import streamlit as st
import pandas as pd
import re
import base64
from datetime import datetime
from collections import Counter

# Try importing NLP libraries with error handling
try:
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer
    from textblob import TextBlob
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as VaderAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False

# Try importing visualization libraries
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

# Download NLTK data
@st.cache_resource
def download_nltk_data():
    if not NLP_AVAILABLE:
        return False
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('brown', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        return True
    except Exception:
        return False

nltk_success = download_nltk_data() if NLP_AVAILABLE else False

# Initialize VADER
@st.cache_resource
def get_vader_analyzer():
    if VADER_AVAILABLE:
        return VaderAnalyzer()
    elif NLP_AVAILABLE and nltk_success:
        return SentimentIntensityAnalyzer()
    return None

vader = get_vader_analyzer()

# Page configuration
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .feedback-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    .positive {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .neutral {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .negative {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .metric-card {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .emoji-large {
        font-size: 48px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'feedback_history' not in st.session_state:
    st.session_state.feedback_history = []
if 'total_analyses' not in st.session_state:
    st.session_state.total_analyses = 0

# Enhanced keyword-based sentiment analysis
def analyze_sentiment_keywords(text):
    """Enhanced keyword-based sentiment analysis with context"""
    text_lower = text.lower()
    
    # Positive words with intensity weights
    positive_words = {
        'excellent': 1.0, 'amazing': 1.0, 'outstanding': 1.0, 'perfect': 0.9,
        'brilliant': 0.9, 'fantastic': 0.9, 'wonderful': 0.9, 'superb': 0.9,
        'great': 0.7, 'good': 0.5, 'love': 0.8, 'happy': 0.7, 'pleased': 0.6,
        'satisfied': 0.6, 'awesome': 0.9, 'impressive': 0.8, 'recommend': 0.7,
        'enjoy': 0.6, 'delighted': 0.8, 'thank': 0.5, 'thanks': 0.5,
        'helpful': 0.6, 'best': 0.8, 'favorite': 0.7, 'incredible': 0.9,
        'exceptional': 0.9, 'remarkable': 0.8, 'phenomenal': 1.0,
        'nice': 0.4, 'decent': 0.3, 'fine': 0.2, 'okay': 0.1,
        'well': 0.3, 'better': 0.5, 'improved': 0.6, 'smooth': 0.5,
        'easy': 0.4, 'simple': 0.3, 'clear': 0.4, 'fast': 0.5
    }
    
    # Negative words with intensity weights
    negative_words = {
        'terrible': -1.0, 'horrible': -1.0, 'awful': -1.0, 'disgusting': -1.0,
        'worst': -0.9, 'hate': -0.9, 'useless': -0.9, 'pathetic': -0.9,
        'bad': -0.5, 'poor': -0.6, 'disappointed': -0.7, 'disappointing': -0.7,
        'boring': -0.6, 'slow': -0.5, 'broken': -0.8, 'failed': -0.8,
        'failure': -0.8, 'problem': -0.6, 'issue': -0.5, 'complaint': -0.6,
        'unhappy': -0.7, 'frustrated': -0.7, 'angry': -0.8, 'rude': -0.8,
        'expensive': -0.4, 'overpriced': -0.6, 'waste': -0.7, 'never': -0.5,
        'annoying': -0.6, 'difficult': -0.5, 'hard': -0.3, 'confusing': -0.5,
        'ugly': -0.7, 'stupid': -0.8, 'ridiculous': -0.7, 'unacceptable': -0.8,
        'mediocre': -0.4, 'average': -0.1, 'ok': 0.0, 'nothing': -0.2,
        'lack': -0.3, 'missing': -0.4, 'error': -0.5, 'bug': -0.5
    }
    
    # Intensifiers and negations
    intensifiers = ['very', 'really', 'extremely', 'absolutely', 'completely', 
                   'totally', 'highly', 'so', 'quite', 'incredibly']
    negations = ['not', 'no', "n't", 'never', 'neither', 'nor', 'hardly', 'barely']
    
    words = text_lower.split()
    total_score = 0
    word_count = 0
    
    for i, word in enumerate(words):
        # Check for negation before the word
        negation_multiplier = 1
        if i > 0 and words[i-1] in negations:
            negation_multiplier = -1
        
        # Check for intensifier before the word
        intensifier_multiplier = 1
        if i > 0 and words[i-1] in intensifiers:
            intensifier_multiplier = 1.5
        
        if word in positive_words:
            total_score += positive_words[word] * negation_multiplier * intensifier_multiplier
            word_count += 1
        elif word in negative_words:
            total_score += negative_words[word] * negation_multiplier * intensifier_multiplier
            word_count += 1
    
    # Normalize score
    if word_count > 0:
        avg_score = total_score / word_count
    else:
        avg_score = 0
    
    # Determine sentiment
    if avg_score > 0.15:
        sentiment = "Positive"
        emoji = "😊"
        confidence = min(abs(avg_score) * 100, 95)
        polarity = min(avg_score, 0.95)
    elif avg_score < -0.15:
        sentiment = "Negative"
        emoji = "😞"
        confidence = min(abs(avg_score) * 100, 95)
        polarity = max(avg_score, -0.95)
    else:
        sentiment = "Neutral"
        emoji = "😐"
        confidence = 50 + (abs(avg_score) * 30)
        polarity = avg_score
    
    return {
        'sentiment': sentiment,
        'emoji': emoji,
        'polarity': round(polarity, 3),
        'subjectivity': min(word_count / max(len(words), 1), 0.9),
        'confidence': round(confidence, 2)
    }

# VADER Analysis (better for short texts)
def analyze_sentiment_vader(text):
    """Analyze sentiment using VADER"""
    if vader:
        scores = vader.polarity_scores(text)
        compound = scores['compound']
        
        # VADER compound score ranges from -1 to 1
        if compound >= 0.05:
            sentiment = "Positive"
            emoji = "😊"
            confidence = min(abs(compound) * 100, 95)
        elif compound <= -0.05:
            sentiment = "Negative"
            emoji = "😞"
            confidence = min(abs(compound) * 100, 95)
        else:
            sentiment = "Neutral"
            emoji = "😐"
            confidence = 50 - (abs(compound) * 30)
        
        return {
            'sentiment': sentiment,
            'emoji': emoji,
            'polarity': round(compound, 3),
            'subjectivity': (scores['pos'] + scores['neg']) / max(scores['neu'], 0.1),
            'confidence': round(confidence, 2)
        }
    return analyze_sentiment_keywords(text)

# TextBlob Analysis
def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob"""
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.15:
            sentiment = "Positive"
            emoji = "😊"
            confidence = min(abs(polarity) * 100, 95)
        elif polarity < -0.15:
            sentiment = "Negative"
            emoji = "😞"
            confidence = min(abs(polarity) * 100, 95)
        else:
            sentiment = "Neutral"
            emoji = "😐"
            confidence = 50 + (abs(polarity) * 30)
        
        return {
            'sentiment': sentiment,
            'emoji': emoji,
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'confidence': round(confidence, 2)
        }
    except Exception:
        return analyze_sentiment_keywords(text)

# Ensemble analysis (combine multiple methods)
def analyze_sentiment(text):
    """Main sentiment analysis using ensemble of methods"""
    # Get results from different methods
    vader_result = analyze_sentiment_vader(text)
    
    if NLP_AVAILABLE:
        try:
            textblob_result = analyze_sentiment_textblob(text)
            
            # Ensemble: average the results
            avg_polarity = (vader_result['polarity'] + textblob_result['polarity']) / 2
            avg_subjectivity = (vader_result['subjectivity'] + textblob_result['subjectivity']) / 2
            avg_confidence = (vader_result['confidence'] + textblob_result['confidence']) / 2
            
            # Determine final sentiment
            if avg_polarity > 0.1:
                sentiment = "Positive"
                emoji = "😊"
                confidence = min(avg_confidence, 95)
            elif avg_polarity < -0.1:
                sentiment = "Negative"
                emoji = "😞"
                confidence = min(avg_confidence, 95)
            else:
                sentiment = "Neutral"
                emoji = "😐"
                confidence = 50 + (abs(avg_polarity) * 20)
            
            return {
                'sentiment': sentiment,
                'emoji': emoji,
                'polarity': round(avg_polarity, 3),
                'subjectivity': round(avg_subjectivity, 3),
                'confidence': round(confidence, 2),
                'vader_score': vader_result['polarity'],
                'textblob_score': textblob_result['polarity']
            }
        except Exception:
            return vader_result
    else:
        return vader_result

def extract_keywords(text):
    """Extract keywords with emotions"""
    emotions = {
        'happy': '😊', 'sad': '😢', 'angry': '😠', 'love': '❤️',
        'great': '👍', 'bad': '👎', 'amazing': '✨', 'terrible': '💔',
        'good': '✅', 'poor': '❌', 'excellent': '🌟', 'awful': '😱'
    }
    
    words = re.findall(r'\b\w+\b', text.lower())
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                  'should', 'may', 'might', 'can', 'i', 'you', 'he', 'she', 'it', 'we',
                  'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its',
                  'our', 'their', 'this', 'that', 'these', 'those', 'am'}
    
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    word_counts = Counter(keywords).most_common(15)
    
    # Add emotion emojis if available
    enhanced_keywords = []
    for word, count in word_counts:
        em = emotions.get(word, '')
        enhanced_keywords.append((f"{em} {word}" if em else word, count))
    
    return enhanced_keywords

def generate_wordcloud(feedback_list):
    """Generate word cloud from feedback"""
    if not WORDCLOUD_AVAILABLE or not feedback_list:
        return None
    
    try:
        all_text = ' '.join([fb['text'] for fb in feedback_list])
        wordcloud = WordCloud(width=800, height=400, background_color='white', 
                             max_words=100, collocations=False).generate(all_text)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        return fig
    except Exception:
        return None

# Main Header
st.markdown('<div class="main-header"><h1>🎯 Customer Feedback Sentiment Analysis</h1><p>Multi-Model AI-Powered Feedback Classification System</p></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard Controls")
    
    analysis_mode = st.radio(
        "Choose Mode",
        ["🎯 Single Analysis", "📝 Batch Analysis", "📊 View History"],
        key="analysis_mode"
    )
    
    st.markdown("---")
    
    # Statistics
    st.subheader("📈 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Analyses", st.session_state.total_analyses)
    with col2:
        if st.session_state.feedback_history:
            positive_count = sum(1 for fb in st.session_state.feedback_history if fb['sentiment'] == 'Positive')
            st.metric("Positive Rate", f"{(positive_count/len(st.session_state.feedback_history)*100):.1f}%")
        else:
            st.metric("Positive Rate", "0%")
    
    st.markdown("---")
    
    if st.session_state.feedback_history:
        st.subheader("💾 Export Data")
        df_export = pd.DataFrame(st.session_state.feedback_history)
        csv = df_export.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="feedback_history.csv">📥 Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔧 System Status")
    if vader:
        st.success("✅ VADER Active (Best accuracy)")
    elif NLP_AVAILABLE and nltk_success:
        st.success("✅ NLP Active")
    else:
        st.warning("⚡ Enhanced Keyword Mode")
    
    # Example feedbacks
    st.markdown("---")
    st.subheader("🧪 Test Examples")
    st.caption("Click to copy example feedbacks")
    examples = [
        "This product is absolutely amazing! Best purchase ever!",
        "The service was terrible, very disappointed with the quality.",
        "It's okay, nothing special but gets the job done.",
        "I love this! Excellent customer support and fast delivery.",
        "Waste of money, broken on arrival. Very frustrating experience.",
        "Average product, decent quality for the price."
    ]
    for ex in examples:
        if st.button(ex[:80] + "...", key=ex[:20]):
            st.session_state.example_feedback = ex

# Main Content Area
if analysis_mode == "🎯 Single Analysis":
    st.header("Single Feedback Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Use example if selected
        default_text = st.session_state.get('example_feedback', '')
        feedback_text = st.text_area(
            "Enter Customer Feedback:",
            placeholder="Type or paste customer feedback here...",
            height=150,
            key="single_feedback",
            value=default_text
        )
        
        customer_name = st.text_input("Customer Name (Optional):", placeholder="Enter name...")
        
        if st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True):
            if feedback_text.strip():
                with st.spinner("Analyzing with multiple models..."):
                    result = analyze_sentiment(feedback_text)
                    keywords = extract_keywords(feedback_text)
                    
                    feedback_record = {
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'customer': customer_name if customer_name else "Anonymous",
                        'text': feedback_text,
                        'sentiment': result['sentiment'],
                        'emoji': result['emoji'],
                        'polarity': result['polarity'],
                        'subjectivity': result['subjectivity'],
                        'confidence': result['confidence']
                    }
                    st.session_state.feedback_history.append(feedback_record)
                    st.session_state.total_analyses += 1
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("### 📊 Analysis Result")
                    
                    res_col1, res_col2, res_col3 = st.columns(3)
                    
                    with res_col1:
                        sentiment_color = "green" if result['sentiment'] == "Positive" else "red" if result['sentiment'] == "Negative" else "orange"
                        bg_color = '#d4edda' if result['sentiment'] == 'Positive' else '#f8d7da' if result['sentiment'] == 'Negative' else '#fff3cd'
                        st.markdown(f"""
                            <div class="metric-card" style="background-color: {bg_color}">
                                <h3>Overall Sentiment</h3>
                                <div class="emoji-large">{result['emoji']}</div>
                                <h2 style="color: {sentiment_color};">{result['sentiment']}</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with res_col2:
                        st.markdown(f"""
                            <div class="metric-card" style="background-color: #e7f3ff;">
                                <h3>Confidence Score</h3>
                                <div style="font-size: 48px;">📊</div>
                                <h2>{result['confidence']}%</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with res_col3:
                        st.markdown(f"""
                            <div class="metric-card" style="background-color: #f0e6ff;">
                                <h3>Subjectivity</h3>
                                <div style="font-size: 48px;">🎯</div>
                                <h2>{(result['subjectivity']*100):.1f}%</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Show model scores if available
                    if 'vader_score' in result and 'textblob_score' in result:
                        st.markdown("---")
                        st.subheader("🔬 Individual Model Scores")
                        model_col1, model_col2, model_col3 = st.columns(3)
                        
                        with model_col1:
                            st.metric("VADER Score", f"{result['vader_score']:.3f}", 
                                     delta="Best for social media")
                        
                        with model_col2:
                            st.metric("TextBlob Score", f"{result['textblob_score']:.3f}",
                                     delta="Best for paragraphs")
                        
                        with model_col3:
                            st.metric("Ensemble Score", f"{result['polarity']:.3f}",
                                     delta="Combined result")
                    
                    # Polarity gauge
                    st.markdown("---")
                    st.subheader("📈 Sentiment Polarity Meter")
                    
                    if PLOTLY_AVAILABLE:
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number+delta",
                            value = result['polarity'],
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Polarity Score (-1 to 1)"},
                            delta = {'reference': 0},
                            gauge = {
                                'axis': {'range': [-1, 1], 'tickwidth': 1},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [-1, -0.5], 'color': "#dc3545"},
                                    {'range': [-0.5, -0.1], 'color': "#ff6b6b"},
                                    {'range': [-0.1, 0.1], 'color': "#ffc107"},
                                    {'range': [0.1, 0.5], 'color': "#51cf66"},
                                    {'range': [0.5, 1], 'color': "#28a745"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': result['polarity']
                                }
                            }
                        ))
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # Simple progress bar
                        polarity_normalized = (result['polarity'] + 1) / 2
                        st.progress(polarity_normalized)
                        color = "green" if result['polarity'] > 0.1 else "red" if result['polarity'] < -0.1 else "orange"
                        st.markdown(f"**Polarity Score:** :{color}[{result['polarity']:.3f}]")
                    
                    # Keywords
                    if keywords:
                        st.markdown("---")
                        st.subheader("🏷️ Key Terms & Emotions")
                        cols = st.columns(5)
                        for i, (word, count) in enumerate(keywords[:10]):
                            with cols[i % 5]:
                                st.metric(f"#{i+1}", word, count)
                    
                    st.success("✅ Analysis complete with ensemble methods!")
            else:
                st.warning("⚠️ Please enter feedback text to analyze.")
    
    with col2:
        st.info("""
        ### 💡 Detection Methods Used
        
        **Multi-Model Ensemble:**
        1. 🎯 **VADER** - Best for short social media texts
        2. 📚 **TextBlob** - Good for longer paragraphs
        3. 🔤 **Keyword Analysis** - Context-aware fallback
        
        ### 🎨 Classification Scale
        - **😊 Positive**: Polarity > 0.1
        - **😐 Neutral**: -0.1 to 0.1  
        - **😞 Negative**: Polarity < -0.1
        
        ### ✨ Features
        - Negation detection ("not good" ≠ "good")
        - Intensity modifiers ("very bad" > "bad")
        - Context-aware analysis
        """)
        
        # Quick test examples
        st.markdown("---")
        st.subheader("🧪 Quick Test")
        test_texts = {
            "Strong Positive": "I absolutely love this! Best experience ever!",
            "Mild Positive": "It's pretty good, I'm satisfied with it.",
            "Neutral": "The product arrived today. It is what I ordered.",
            "Mild Negative": "Not great, could be better.",
            "Strong Negative": "Terrible experience! Worst product ever!"
        }
        
        for label, text in test_texts.items():
            if st.button(f"Test: {label}", key=label):
                result = analyze_sentiment(text)
                st.success(f"Result: {result['emoji']} {result['sentiment']} ({result['confidence']}% confidence)")

elif analysis_mode == "📝 Batch Analysis":
    st.header("Batch Feedback Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        batch_text = st.text_area(
            "Paste Multiple Feedbacks (one per line):",
            placeholder="Product is amazing!\nService could be better\nAverage experience...",
            height=200,
            key="batch_feedback"
        )
        
        if st.button("📊 Analyze Batch", type="primary", use_container_width=True):
            if batch_text.strip():
                feedbacks = [line.strip() for line in batch_text.split('\n') if line.strip()]
                
                if feedbacks:
                    with st.spinner(f"Analyzing {len(feedbacks)} feedbacks with ensemble methods..."):
                        results = []
                        for feedback in feedbacks:
                            result = analyze_sentiment(feedback)
                            results.append({
                                'Feedback': feedback[:100] + "..." if len(feedback) > 100 else feedback,
                                'Sentiment': result['sentiment'],
                                'Emoji': result['emoji'],
                                'Confidence': f"{result['confidence']}%",
                                'Polarity': result['polarity']
                            })
                            
                            feedback_record = {
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'customer': 'Batch',
                                'text': feedback,
                                'sentiment': result['sentiment'],
                                'emoji': result['emoji'],
                                'polarity': result['polarity'],
                                'subjectivity': result['subjectivity'],
                                'confidence': result['confidence']
                            }
                            st.session_state.feedback_history.append(feedback_record)
                            st.session_state.total_analyses += 1
                        
                        st.markdown("### 📊 Batch Results")
                        df = pd.DataFrame(results)
                        st.dataframe(df, use_container_width=True)
                        
                        sentiment_counts = df['Sentiment'].value_counts()
                        
                        chart_col1, chart_col2 = st.columns(2)
                        
                        with chart_col1:
                            st.subheader("Sentiment Distribution")
                            if PLOTLY_AVAILABLE:
                                fig = px.pie(
                                    values=sentiment_counts.values,
                                    names=sentiment_counts.index,
                                    color=sentiment_counts.index,
                                    color_discrete_map={
                                        'Positive': '#28a745',
                                        'Neutral': '#ffc107',
                                        'Negative': '#dc3545'
                                    },
                                    hole=0.4
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.bar_chart(sentiment_counts)
                        
                        with chart_col2:
                            st.subheader("Confidence Distribution")
                            if PLOTLY_AVAILABLE:
                                fig = px.histogram(
                                    df, 
                                    x='Sentiment',
                                    color='Sentiment',
                                    color_discrete_map={
                                        'Positive': '#28a745',
                                        'Neutral': '#ffc107',
                                        'Negative': '#dc3545'
                                    }
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.bar_chart(df['Sentiment'].value_counts())
                        
                        st.success(f"✅ Successfully analyzed {len(feedbacks)} feedbacks!")
                else:
                    st.warning("⚠️ No valid feedback found.")
            else:
                st.warning("⚠️ Please enter feedback text.")
    
    with col2:
        st.info("""
        ### 📝 Batch Analysis Tips
        
        - One feedback per line
        - Empty lines ignored
        - Each line gets ensemble analysis
        
        ### 📊 Results Include:
        - Individual sentiment scores
        - Distribution charts
        - Confidence levels
        - Exportable data
        """)

else:  # View History
    st.header("📊 Feedback Analysis History")
    
    if st.session_state.feedback_history:
        df_history = pd.DataFrame(st.session_state.feedback_history)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            sentiment_filter = st.multiselect(
                "Filter by Sentiment:",
                options=["Positive", "Neutral", "Negative"],
                default=["Positive", "Neutral", "Negative"]
            )
        
        with col2:
            if 'customer' in df_history.columns:
                customers = ['All'] + list(df_history['customer'].unique())
                customer_filter = st.selectbox("Filter by Customer:", customers)
        
        with col3:
            if len(df_history) > 0:
                min_conf = float(df_history['confidence'].min())
                max_conf = float(df_history['confidence'].max())
                confidence_range = st.slider(
                    "Min Confidence %:",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=5.0
                )
        
        # Apply filters
        filtered_df = df_history[df_history['sentiment'].isin(sentiment_filter)]
        if 'customer' in filtered_df.columns and 'customer_filter' in locals() and customer_filter != 'All':
            filtered_df = filtered_df[filtered_df['customer'] == customer_filter]
        if 'confidence_range' in locals():
            filtered_df = filtered_df[filtered_df['confidence'] >= confidence_range]
        
        # Statistics
        st.markdown("---")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("Total Feedbacks", len(filtered_df))
        
        with stat_col2:
            positive_count = len(filtered_df[filtered_df['sentiment'] == 'Positive'])
            st.metric("😊 Positive", positive_count)
        
        with stat_col3:
            neutral_count = len(filtered_df[filtered_df['sentiment'] == 'Neutral'])
            st.metric("😐 Neutral", neutral_count)
        
        with stat_col4:
            negative_count = len(filtered_df[filtered_df['sentiment'] == 'Negative'])
            st.metric("😞 Negative", negative_count)
        
        # Charts
        st.markdown("---")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("Sentiment Distribution")
            if PLOTLY_AVAILABLE:
                fig = px.pie(
                    filtered_df,
                    names='sentiment',
                    color='sentiment',
                    color_discrete_map={
                        'Positive': '#28a745',
                        'Neutral': '#ffc107',
                        'Negative': '#dc3545'
                    },
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                sentiment_counts = filtered_df['sentiment'].value_counts()
                st.bar_chart(sentiment_counts)
        
        with chart_col2:
            st.subheader("Confidence Distribution")
            if PLOTLY_AVAILABLE:
                filtered_df_copy = filtered_df.copy()
                filtered_df_copy['timestamp'] = pd.to_datetime(filtered_df_copy['timestamp'])
                fig = px.scatter(
                    filtered_df_copy,
                    x='timestamp',
                    y='confidence',
                    color='sentiment',
                    color_discrete_map={
                        'Positive': '#28a745',
                        'Neutral': '#ffc107',
                        'Negative': '#dc3545'
                    },
                    size='confidence',
                    hover_data=['text']
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Install plotly for advanced charts")
        
        # Word Cloud
        st.markdown("---")
        st.subheader("☁️ Feedback Word Cloud")
        wordcloud_fig = generate_wordcloud(st.session_state.feedback_history)
        if wordcloud_fig:
            st.pyplot(wordcloud_fig)
        else:
            st.info("Install wordcloud for this visualization")
        
        # Feedback list
        st.markdown("---")
        st.subheader("📋 Feedback Details")
        
        for i, row in filtered_df.iterrows():
            sentiment_class = row['sentiment'].lower()
            st.markdown(f"""
                <div class="feedback-card {sentiment_class}">
                    <h4>{row['emoji']} {row['sentiment']} (Confidence: {row['confidence']}%)</h4>
                    <p><strong>Customer:</strong> {row['customer']}</p>
                    <p><strong>Time:</strong> {row['timestamp']}</p>
                    <p><strong>Feedback:</strong> {row['text'][:200]}...</p>
                    <p><small>Polarity: {row['polarity']:.3f} | Subjectivity: {row['subjectivity']:.3f}</small></p>
                </div>
            """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.feedback_history = []
            st.session_state.total_analyses = 0
            st.rerun()
    else:
        st.info("📭 No feedback history yet. Start analyzing feedbacks!")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🎯 Enhanced Sentiment Analysis Dashboard | Multi-Model Ensemble System</p>
        <p>Powered by VADER • TextBlob • Enhanced Keyword Analysis</p>
    </div>
""", unsafe_allow_html=True)
