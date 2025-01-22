# Subdomain Parser Bot

This project is a **Python-based bot** designed to parse subdomains from websites, using `suip.biz` services to extract subdomains and analyze them for status codes. It includes features such as rotating proxies, status code checking, and error handling to work efficiently.

## Features

- **Subdomain Parsing**: Retrieves subdomains for given domains using services inside `suip.biz` like `findomain` and `subfinder`.
- **Rotating Proxies**: Utilizes a proxy list to avoid being blocked by the target website.
- **Status Code Validation**: Checks the HTTP status codes of parsed subdomains.
- **Request Resilience**: Implements error handling for network issues and unexpected responses.
- **Integration with Telegram Bot**: Provides an interface for interacting with the parser through Telegram.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add a proxy list file:
   Create a `proxy.txt` file in the root directory, with one proxy per line in the format:
   ```
   ip:port:username:password
   ```

## Usage

1. **Run the Parser Script**:
   Use the `parser.py` script to parse subdomains:
   ```bash
   python scripts/parser.py
   ```

2. **Configure and Run the Telegram Bot**:
   Update the `bot` configuration to include your Telegram bot token and webhook settings, then start the bot:
   ```bash
   python bot/main.py
   ```

3. **Example Functionality**:
   - Pass a domain and action (`findomain` or `subfinder`) to extract subdomains:
     ```python
     from parser import parse_suip_biz
     proxies = load_proxies()
     subdomains = parse_suip_biz("example.com", "findomain", proxies)
     print(subdomains)
     ```

## Project Structure

```plaintext
.
├── bot/
│   ├── main.py            		  # Telegram bot entry point
│   ├── handlers/          		  # Handlers for bot logic
│   └── scripts/
│       ├── parser.py      		  # Main subdomain parsing logic
│       ├── checker.py     		  # Script for running parser.py specific commands on deployed server
│       ├── tools_executor.py             # Script for running server installed tools
├── proxy.txt              		  # List of proxies
├── requirements.txt       		  # Dependencies for the project
├── README.md              		  # Project documentation
```

## Requirements

- Python 3.7 or newer
- Libraries (see `requirements.txt`):
  - `requests`
  - `beautifulsoup4`
  - `urllib3`
  - `requests-html`
  - `telebot`
