<FILE_DOWNLOAD name="README.md">
# SEO URL Checker

A Streamlit web application for analyzing URLs and checking essential SEO elements in bulk or individually.

## Features

- **Single URL Analysis** - Analyze individual URLs for SEO issues
- **CSV Bulk Analysis** - Upload a CSV file to analyze multiple URLs at once
- **Comprehensive SEO Checks**:
  - HTTP status codes
  - Canonical tag validation (self-referring check)
  - Noindex/Nofollow meta tag detection
  - Meta title and description analysis with length validation
  - Color-coded results for quick issue identification

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install streamlit requests beautifulsoup4 pandas
```

## Usage

1. Run the application:
```bash
streamlit run url_checker_app.py
```

2. Open your browser and navigate to the provided local URL (typically `http://localhost:8501`)

3. Choose your analysis method:
   - **Single URL**: Enter a URL and click "Analyze URL"
   - **CSV Upload**: Upload a CSV file with URLs (column should be named 'url', 'URL', 'link', or 'links')

## CSV Format

Your CSV file should contain a column with URLs:
```csv
url
https://example.com
https://google.com
https://github.com
```

## Output

The tool provides:
- ✅ **Green indicators**: Good SEO practices
- ❌ **Red indicators**: Issues that need attention
- ⚠️ **Yellow indicators**: Warnings or suboptimal settings
- Downloadable CSV results for bulk analysis
- Summary statistics

## Requirements

- Python 3.7+
- streamlit
- requests
- beautifulsoup4
- pandas

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</FILE_DOWNLOAD>

Here's your README.md file with the complete MIT License! Click the download link above to save it to your Downloads folder. The file includes:

- Project description and features
- Installation instructions
- Usage guide
- CSV format example
- Requirements list
- Full MIT License text

The README is ready to use with your SEO URL Checker project.
