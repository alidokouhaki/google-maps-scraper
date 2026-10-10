<div align="center">

# 📍 Google Maps Directory Scraper

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33.svg?logo=playwright&logoColor=white)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*A simple, powerful, and elegant tool for extracting business information directly from Google Maps into organized Excel files.*

</div>

---

## ✨ Features

- 🏢 **Effortless Extraction:** Extract comprehensive business data just by specifying a city and a category.
- 🎨 **Modern UI:** Built with Streamlit for a clean, user-friendly, and interactive experience.
- 📊 **Excel Export:** Automatically formats and exports the extracted data into a beautifully structured `.xlsx` file.
- ⚡ **Automated Navigation:** Uses Playwright for fast browsing and automated interactions.

---

## 📋 What It Extracts

For every business found, the scraper retrieves:

| Data Point | Description |
| :--- | :--- |
| 🏷️ **Name** | The official business name |
| ⭐ **Rating** | Average Google Maps rating |
| 💬 **Reviews** | Total number of reviews |
| 📂 **Category** | Primary business category |
| 📍 **Address** | Full physical address |
| 📞 **Phone** | Contact phone number |
| 🌐 **Website** | Link to the business website |
| 🕒 **Status** | Current operating status (Open/Closed) |

---

## ⚙️ Prerequisites

Before you begin, ensure you have met the following requirements:
- 🐍 **Python 3.10** or higher installed on your machine.

---

## 🚀 Installation & Setup

1. **Clone the repository** (or download the ZIP file):
   ```bash
   git clone https://github.com/alidokouhaki/google-maps-scraper.git
   cd google-maps-scraper
   ```

2. **Install the required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the Playwright browser binaries**:
   ```bash
   playwright install chromium
   ```

---

## 🎮 How to Use

1. Launch the Streamlit application from your terminal:
   ```bash
   streamlit run app.py
   ```
2. A web interface will automatically open in your default browser.
3. Enter the **City** (e.g., *Isfahan*, *New York*) and **Business Category** (e.g., *Restaurant*, *Accounting firm*).
4. Click **🚀 Start Scraping** and wait for the magic to happen.
5. Once finished, click **📥 Download Excel File** to get your neatly formatted data!

---

<div align="center">
  <i>Developed with ❤️ for data enthusiasts and researchers.</i>
</div>
