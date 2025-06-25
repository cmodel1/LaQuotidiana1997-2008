import re
from bs4 import BeautifulSoup
def remove_html_tags(text: str) -> str:
    """
    Strip HTML tags from `text`, preserving meaningful whitespace:
    - Converts <br> to single newlines
    - Wraps <p> blocks with blank lines
    - Collapses multiple spaces into one
    - Collapses more than two newlines into exactly two
    """
    # Parse the HTML
    soup = BeautifulSoup(text, 'html.parser')
    # Replace <br> tags with newline characters
    for br in soup.find_all('br'):
        br.replace_with('\n')
    # Wrap each <p> block with newlines
    for p in soup.find_all('p'):
        p.insert_before('\n')
        p.insert_after('\n')
    # Extract text
    extracted = soup.get_text()
    # Normalize whitespace
    # Strip leading/trailing whitespace
    cleaned = extracted.strip()
    # Collapse multiple spaces into one
    cleaned = re.sub(r' +', ' ', cleaned)
    # Collapse more than two newlines into exactly two
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    # Remove spaces around newlines
    cleaned = re.sub(r'[ \t]*\n[ \t]*', '\n', cleaned)
    return cleaned