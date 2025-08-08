import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin, urlparse
import time
import re
from io import StringIO

# Set page configuration
st.set_page_config(
    page_title="SEO URL Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
.status-200 {
    color: white;
    background-color: #28a745;
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: bold;
}

.status-error {
    color: white;
    background-color: #dc3545;
    padding: 5px 10px;
    border-radius: 5px;
    font-weight: bold;
}

.tag-good {
    color: white;
    background-color: #28a745;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 12px;
}

.tag-bad {
    color: white;
    background-color: #dc3545;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 12px;
}

.tag-warning {
    color: white;
    background-color: #ffc107;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 12px;
    color: black;
}

.error-message {
    color: #dc3545;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

def get_page_data(url):
    """
    Fetch and analyze a single URL for SEO elements
    """
    try:
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Make request with timeout and headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        status_code = response.status_code
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get canonical tag
        canonical_tag = soup.find('link', {'rel': 'canonical'})
        canonical_url = canonical_tag.get('href') if canonical_tag else None
        
        # Check if canonical is self-referring
        if canonical_url:
            # Handle relative URLs
            canonical_url = urljoin(url, canonical_url)
            is_self_referring = canonical_url.rstrip('/') == response.url.rstrip('/')
        else:
            is_self_referring = False
            canonical_url = "Not found"
        
        # Check for noindex
        noindex_found = False
        robots_meta = soup.find('meta', {'name': 'robots'})
        if robots_meta:
            content = robots_meta.get('content', '').lower()
            noindex_found = 'noindex' in content
        
        # Check for nofollow
        nofollow_found = False
        if robots_meta:
            content = robots_meta.get('content', '').lower()
            nofollow_found = 'nofollow' in content
        
        # Get meta title
        title_tag = soup.find('title')
        meta_title = title_tag.get_text().strip() if title_tag else None
        title_length = len(meta_title) if meta_title else 0
        
        # Get meta description
        desc_tag = soup.find('meta', {'name': 'description'})
        meta_description = desc_tag.get('content').strip() if desc_tag else None
        desc_length = len(meta_description) if meta_description else 0
        
        return {
            'url': url,
            'status_code': status_code,
            'canonical_url': canonical_url,
            'is_self_referring': is_self_referring,
            'noindex_found': noindex_found,
            'nofollow_found': nofollow_found,
            'meta_title': meta_title,
            'title_length': title_length,
            'meta_description': meta_description,
            'desc_length': desc_length,
            'error': None
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'status_code': 'Error',
            'canonical_url': 'Error',
            'is_self_referring': False,
            'noindex_found': False,
            'nofollow_found': False,
            'meta_title': None,
            'title_length': 0,
            'meta_description': None,
            'desc_length': 0,
            'error': str(e)
        }
    except Exception as e:
        return {
            'url': url,
            'status_code': 'Error',
            'canonical_url': 'Error',
            'is_self_referring': False,
            'noindex_found': False,
            'nofollow_found': False,
            'meta_title': None,
            'title_length': 0,
            'meta_description': None,
            'desc_length': 0,
            'error': str(e)
        }

def format_status_code(status_code):
    """Format status code with color coding"""
    if status_code == 200:
        return f'<span class="status-200">{status_code}</span>'
    else:
        return f'<span class="status-error">{status_code}</span>'

def format_canonical_status(is_self_referring, canonical_url):
    """Format canonical status with color coding"""
    if canonical_url == "Not found":
        return f'<span class="tag-bad">Not Found</span>'
    elif is_self_referring:
        return f'<span class="tag-good">Self-referring</span>'
    else:
        return f'<span class="tag-bad">Non self-referring</span>'

def format_noindex_status(noindex_found):
    """Format noindex status with color coding"""
    if noindex_found:
        return f'<span class="tag-bad">Present</span>'
    else:
        return f'<span class="tag-good">Not Present</span>'

def format_nofollow_status(nofollow_found):
    """Format nofollow status with color coding"""
    if nofollow_found:
        return f'<span class="tag-bad">Present</span>'
    else:
        return f'<span class="tag-good">Not Present</span>'

def format_meta_content(content, length, field_name):
    """Format meta content with length and error handling"""
    if content:
        # Color code length based on SEO best practices
        if field_name == "title":
            if 30 <= length <= 60:
                length_color = "tag-good"
            elif length < 30 or length > 60:
                length_color = "tag-warning"
            else:
                length_color = "tag-warning"
        else:  # description
            if 120 <= length <= 160:
                length_color = "tag-good"
            elif length < 120 or length > 160:
                length_color = "tag-warning"
            else:
                length_color = "tag-warning"
        
        return f'{content[:100]}{"..." if len(content) > 100 else ""} <span class="{length_color}">({length} chars)</span>'
    else:
        return f'<span class="error-message">❌ Missing {field_name}</span>'

# Sidebar navigation
st.sidebar.title("🔍 SEO URL Checker")
st.sidebar.markdown("---")

check_type = st.sidebar.radio(
    "Choose checking method:",
    ["Single URL", "CSV Upload"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 Analysis Includes:
- **Status Code**: HTTP response status
- **Canonical Tag**: Self-referring validation
- **Noindex Tag**: Search engine indexing
- **Nofollow Tag**: Link following permissions
- **Meta Title**: Title tag and length
- **Meta Description**: Description and length

### 🎯 Color Coding:
- 🟢 **Green**: Good/Present when needed
- 🔴 **Red**: Issues/Present when not needed
- 🟡 **Yellow**: Warnings/Suboptimal length
""")

# Main content
st.title("🔍 SEO URL Checker")
st.markdown("---")

if check_type == "Single URL":
    st.subheader("📍 Single URL Analysis")
    
    # URL input
    url_input = st.text_input(
        "Enter URL to analyze:",
        placeholder="https://example.com or example.com",
        help="Enter a complete URL or domain name"
    )
    
    if st.button("🚀 Analyze URL", type="primary"):
        if url_input.strip():
            with st.spinner(f"Analyzing {url_input}..."):
                result = get_page_data(url_input.strip())
                
                if result['error']:
                    st.error(f"Error analyzing URL: {result['error']}")
                else:
                    # Display results in a nice format
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📊 Technical Status")
                        st.markdown(f"**URL:** {result['url']}")
                        st.markdown(f"**Status Code:** {format_status_code(result['status_code'])}", unsafe_allow_html=True)
                        st.markdown(f"**Canonical:** {format_canonical_status(result['is_self_referring'], result['canonical_url'])}", unsafe_allow_html=True)
                        if not result['is_self_referring'] and result['canonical_url'] != "Not found":
                            st.markdown(f"*Canonical URL: {result['canonical_url']}*")
                    
                    with col2:
                        st.markdown("### 🤖 Robot Directives")
                        st.markdown(f"**Noindex:** {format_noindex_status(result['noindex_found'])}", unsafe_allow_html=True)
                        st.markdown(f"**Nofollow:** {format_nofollow_status(result['nofollow_found'])}", unsafe_allow_html=True)
                    
                    st.markdown("### 📝 Meta Information")
                    st.markdown(f"**Title:** {format_meta_content(result['meta_title'], result['title_length'], 'title')}", unsafe_allow_html=True)
                    st.markdown(f"**Description:** {format_meta_content(result['meta_description'], result['desc_length'], 'description')}", unsafe_allow_html=True)
        else:
            st.warning("Please enter a URL to analyze!")

else:  # CSV Upload
    st.subheader("📊 CSV Bulk Analysis")
    
    # CSV upload
    uploaded_file = st.file_uploader(
        "Upload CSV file with URLs",
        type=['csv'],
        help="CSV should have a column named 'url' or 'URL'"
    )
    
    # Sample CSV download
    sample_csv = "url\nhttps://example.com\nhttps://google.com\nhttps://github.com"
    st.download_button(
        label="📥 Download Sample CSV",
        data=sample_csv,
        file_name="sample_urls.csv",
        mime="text/csv"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            # Find URL column
            url_column = None
            for col in df.columns:
                if col.lower() in ['url', 'urls', 'link', 'links']:
                    url_column = col
                    break
            
            if url_column is None:
                st.error("No URL column found. Please ensure your CSV has a column named 'url', 'URL', 'link', or 'links'.")
            else:
                urls = df[url_column].dropna().tolist()
                st.success(f"Found {len(urls)} URLs to analyze")
                
                if st.button("🚀 Analyze All URLs", type="primary"):
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, url in enumerate(urls):
                        status_text.text(f"Analyzing {i+1}/{len(urls)}: {url}")
                        result = get_page_data(url)
                        results.append(result)
                        progress_bar.progress((i + 1) / len(urls))
                        time.sleep(0.5)  # Be nice to servers
                    
                    status_text.text("Analysis complete!")
                    
                    # Create results DataFrame
                    results_df = pd.DataFrame(results)
                    
                    # Display results table
                    st.markdown("### 📋 Analysis Results")
                    
                    # Create formatted HTML table
                    html_table = "<table style='width:100%; border-collapse: collapse;'>"
                    html_table += """
                    <tr style='background-color: #f8f9fa; border: 1px solid #ddd;'>
                        <th style='padding: 12px; border: 1px solid #ddd;'>URL</th>
                        <th style='padding: 12px; border: 1px solid #ddd;'>Status</th>
                        <th style='padding: 12px; border: 1px solid #ddd;'>Canonical</th>
                        <th style='padding: 12px; border: 1px solid #ddd;'>Noindex</th>
                        <th style='padding: 12px; border: 1px solid #ddd;'>Nofollow</th>
                        <th style='padding: 12px; border: 1px solid #ddd;'>Title</th>
                        <th style='padding: 12px; border: 1px solid #ddd;'>Description</th>
                    </tr>
                    """
                    
                    for _, row in results_df.iterrows():
                        html_table += "<tr style='border: 1px solid #ddd;'>"
                        html_table += f"<td style='padding: 8px; border: 1px solid #ddd; max-width: 200px; word-break: break-all;'>{row['url']}</td>"
                        html_table += f"<td style='padding: 8px; border: 1px solid #ddd; text-align: center;'>{format_status_code(row['status_code'])}</td>"
                        html_table += f"<td style='padding: 8px; border: 1px solid #ddd; text-align: center;'>{format_canonical_status(row['is_self_referring'], row['canonical_url'])}</td>"
                        html_table += f"<td style='padding: 8px; border: 1px solid #ddd; text-align: center;'>{format_noindex_status(row['noindex_found'])}</td>"
                        html_table += f"<td style='padding: 8px; border: 1px solid #ddd; text-align: center;'>{format_nofollow_status(row['nofollow_found'])}</td>"
                        html_table += f"<td style='padding: 8px; border: 1px solid #ddd; max-width: 300px;'>{format_meta_content(row['meta_title'], row['title_length'], 'title')}</td>"
                        html_table += f"<td style='padding: 8px; border: 1px solid #ddd; max-width: 300px;'>{format_meta_content(row['meta_description'], row['desc_length'], 'description')}</td>"
                        html_table += "</tr>"
                    
                    html_table += "</table>"
                    
                    st.markdown(html_table, unsafe_allow_html=True)
                    
                    # Download results
                    csv = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv,
                        file_name=f"seo_analysis_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Summary statistics
                    st.markdown("### 📈 Summary Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        success_count = len([r for r in results if r['status_code'] == 200])
                        st.metric("✅ Successful Requests", f"{success_count}/{len(results)}")
                    
                    with col2:
                        canonical_issues = len([r for r in results if not r['is_self_referring'] and r['canonical_url'] != "Not found"])
                        st.metric("⚠️ Canonical Issues", canonical_issues)
                    
                    with col3:
                        noindex_count = len([r for r in results if r['noindex_found']])
                        st.metric("🚫 Noindex Pages", noindex_count)
                    
                    with col4:
                        missing_titles = len([r for r in results if not r['meta_title']])
                        st.metric("📝 Missing Titles", missing_titles)
        
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 14px;'>
    Built with ❤️ using Streamlit | SEO URL Checker v1.0
    </div>
    """, 
    unsafe_allow_html=True
)
