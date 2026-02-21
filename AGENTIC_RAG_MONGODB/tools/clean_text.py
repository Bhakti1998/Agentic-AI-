import re
def clean_text(text: str) -> str:
    text = re.sub(r"<\s*(EOS|pad)\s*>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"(Figure|Table)\s+\d+[:.]?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r'\.{2,}', '.', text)

    return text.strip()