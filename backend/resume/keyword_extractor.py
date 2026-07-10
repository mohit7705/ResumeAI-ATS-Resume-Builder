import re


def extract_keywords(job_description: str) -> list[str]:
    text = job_description.lower()

    text = re.sub(r"[^a-z0-9#+.\-\s]", " ", text)
    words = re.findall(r"[a-z0-9#+.\-]+", text)

    stop_words = {
        "the", "a", "an", "and", "or", "to", "for", "of", "in", "on",
        "with", "is", "are", "be", "as", "at", "by", "from", "will",
        "should", "must", "our", "your", "you", "we", "their", "they",
        "have", "has", "had", "looking", "required", "requirement",
        "responsibilities", "responsibility", "experience", "candidate"
    }

    keywords = []

    for word in words:
        if len(word) < 2:
            continue

        if word in stop_words:
            continue

        if word not in keywords:
            keywords.append(word)

    return keywords