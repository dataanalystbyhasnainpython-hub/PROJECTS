import streamlit as st
import pandas as pd
import re
import base64
from datetime import datetime
from collections import Counter

# Try importing NLP libraries with error handling
try:
    import nltk
    from textblob import TextBlob
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

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

# Download NLTK data with error handling
@st.cache_resource
def download_nltk_data():
    if not NLP_AVAILABLE:
        return False
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('brown', quiet=True)
        return True
    except Exception:
        return False

# Initialize NLTK only if available
nltk_success = download_nltk_data() if NLP_AVAILABLE else False

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

# Simple keyword-based sentiment analysis as fallback
def analyze_sentiment_simple(text):
    """Simple keyword-based sentiment analysis (fallback method)"""
    text_lower = text.lower()
    
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 
                     'love', 'happy', 'pleased', 'satisfied', 'awesome', 'brilliant',
                     'outstanding', 'perfect', 'best', 'thank', 'thanks', 'helpful',
                     'impressive', 'recommend', 'enjoy', 'delighted', 'superb']
    
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'poor', 'disappointed',
                     'hate', 'worst', 'useless', 'waste', 'boring', 'slow',
                     'broken', 'failed', 'failure', 'problem', 'issue', 'complaint',
                     'unhappy', 'frustrated', 'angry', 'rude', 'expensive', 'overpriced']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "Positive"
        emoji = "😊"
        confidence = min((positive_count / max(positive_count + negative_count, 1)) * 100, 100)
        polarity = 0.5
    elif negative_count > positive_count:
        sentiment = "Negative"
        emoji = "😞"
        confidence = min((negative_count / max(positive_count + negative_count, 1)) * 100, 100)
        polarity = -0.5
    else:
        sentiment = "Neutral"
        emoji = "😐"
        confidence = 50
        polarity = 0
    
    return {
        'sentiment': sentiment,
        'emoji': emoji,
        'polarity': polarity,
        'subjectivity': 0.5,
        'confidence': round(confidence, 2)
    }

def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        sentiment = "Positive"
        emoji = "😊"
        confidence = min(abs(polarity) * 100, 100)
    elif polarity < -0.1:
        sentiment = "Negative"
        emoji = "😞"
        confidence = min(abs(polarity) * 100, 100)
    else:
        sentiment = "Neutral"
        emoji = "😐"
        confidence = 100 - (abs(polarity) * 100)
    
    return {
        'sentiment': sentiment,
        'emoji': emoji,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'confidence': round(confidence, 2)
    }

# Choose analysis method
def analyze_sentiment(text):
    """Main sentiment analysis function with fallback"""
    if NLP_AVAILABLE and nltk_success:
        try:
            return analyze_sentiment_textblob(text)
        except Exception:
            return analyze_sentiment_simple(text)
    else:
        return analyze_sentiment_simple(text)

def extract_keywords(text):
    """Extract keywords from text"""
    words = re.findall(r'\b\w+\b', text.lower())
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                  'should', 'may', 'might', 'can', 'i', 'you', 'he', 'she', 'it', 'we',
                  'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its',
                  'our', 'their', 'this', 'that', 'these', 'those', 'am', 'very', 'really'}
    
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    return Counter(keywords).most_common(10)

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
st.markdown('<div class="main-header"><h1>🎯 Customer Feedback Sentiment Analysis</h1><p>AI-Powered Real-Time Feedback Classification System</p></div>', unsafe_allow_html=True)

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
    if NLP_AVAILABLE and nltk_success:
        st.success("✅ Advanced NLP Active")
    else:
        st.warning("⚡ Basic NLP Mode")
        st.info("Using keyword-based analysis")

# Main Content Area
if analysis_mode == "🎯 Single Analysis":
    st.header("Single Feedback Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        feedback_text = st.text_area(
            "Enter Customer Feedback:",
            placeholder="Type or paste customer feedback here...",
            height=150,
            key="single_feedback"
        )
        
        customer_name = st.text_input("Customer Name (Optional):", placeholder="Enter name...")
        
        if st.button("🔍 Analyze Sentiment", type="primary", use_container_width=True):
            if feedback_text.strip():
                with st.spinner("Analyzing sentiment..."):
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
                                <h3>Sentiment</h3>
                                <div class="emoji-large">{result['emoji']}</div>
                                <h2 style="color: {sentiment_color};">{result['sentiment']}</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with res_col2:
                        st.markdown(f"""
                            <div class="metric-card" style="background-color: #e7f3ff;">
                                <h3>Confidence</h3>
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
                    
                    # Simple progress bar for polarity
                    st.markdown("---")
                    st.subheader("📈 Sentiment Polarity")
                    polarity_normalized = (result['polarity'] + 1) / 2  # Convert -1 to 1 range to 0 to 1
                    st.progress(polarity_normalized)
                    st.caption(f"Polarity Score: {result['polarity']:.2f} (-1 = Negative, 0 = Neutral, 1 = Positive)")
                    
                    if PLOTLY_AVAILABLE:
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number+delta",
                            value = result['polarity'],
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            title = {'text': "Polarity Score (-1 to 1)"},
                            delta = {'reference': 0},
                            gauge = {
                                'axis': {'range': [-1, 1]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [-1, -0.1], 'color': "#dc3545"},
                                    {'range': [-0.1, 0.1], 'color': "#ffc107"},
                                    {'range': [0.1, 1], 'color': "#28a745"}
                                ]
                            }
                        ))
                        st.plotly_chart(fig, use_container_width=True)
                    
                    if keywords:
                        st.markdown("---")
                        st.subheader("🏷️ Key Terms")
                        cols = st.columns(5)
                        for i, (word, count) in enumerate(keywords[:5]):
                            with cols[i % 5]:
                                st.metric(f"#{i+1}", word.capitalize(), count)
                    
                    st.success("✅ Analysis complete and saved to history!")
            else:
                st.warning("⚠️ Please enter feedback text to analyze.")
    
    with col2:
        st.info("""
        ### 💡 How it works
        
        Our AI analyzes:
        - 😊 **Polarity**: Positive/negative tone
        - 🎯 **Subjectivity**: Factual vs. opinion
        - 📊 **Confidence**: Analysis reliability
        
        ### 🎨 Reaction Scale
        - **😊 Positive**: Polarity > 0.1
        - **😐 Neutral**: -0.1 to 0.1
        - **😞 Negative**: Polarity < -0.1
        
        ### ✨ Tips
        - Use detailed feedback
        - Include emotions
        - Be specific
        """)

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
                    with st.spinner(f"Analyzing {len(feedbacks)} feedbacks..."):
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
                                # Simple bar chart as fallback
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
        ### 📝 Batch Guidelines
        
        - One feedback per line
        - Empty lines will be ignored
        - Each line treated as separate feedback
        
        ### 📊 What you get:
        - Individual analysis
        - Distribution charts
        - Overall sentiment
        - Confidence scores
        """)

else:  # View History
    st.header("📊 Feedback Analysis History")
    
    if st.session_state.feedback_history:
        df_history = pd.DataFrame(st.session_state.feedback_history)
        
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
            sort_by = st.selectbox(
                "Sort by:",
                options=["Timestamp", "Confidence", "Polarity"],
                index=0
            )
        
        filtered_df = df_history[df_history['sentiment'].isin(sentiment_filter)]
        if 'customer' in filtered_df.columns and 'customer_filter' in locals() and customer_filter != 'All':
            filtered_df = filtered_df[filtered_df['customer'] == customer_filter]
        
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
        
        st.markdown("---")
        st.subheader("☁️ Feedback Word Cloud")
        wordcloud_fig = generate_wordcloud(st.session_state.feedback_history)
        if wordcloud_fig:
            st.pyplot(wordcloud_fig)
        else:
            st.info("Install wordcloud for this visualization")
        
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
        <p>🎯 Sentiment Analysis Dashboard | Powered by NLP & Machine Learning</p>
        <p>Built with Streamlit • TextBlob • Plotly</p>
    </div>
""", unsafe_allow_html=True)
