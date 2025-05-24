import re
import yake
import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print("[Extractor] spaCy model load failed:", e)
    nlp = None

class KeywordExtractor:
    def __init__(self):
        self.yake_extractor = yake.KeywordExtractor(lan="en", n=1, top=20)

    def extract_all(self, text: str):
        keywords = set()

        # YAKE!
        try:
            for kw, _ in self.yake_extractor.extract_keywords(text):
                if len(kw) > 1:
                    keywords.add(kw.lower().strip())
        except Exception as e:
            print("[Extractor] YAKE! failed:", e)

        # spaCy
        if nlp:
            try:
                doc = nlp(text)
                for ent in doc.ents:
                    if len(ent.text) > 1:
                        keywords.add(ent.text.lower().strip())
            except Exception as e:
                print("[Extractor] spaCy NER failed:", e)

        # Regex fallback
        try:
            for word in re.findall(r'\b[a-zA-Z0-9]{2,}\b', text):
                keywords.add(word.lower().strip())
        except Exception as e:
            print("[Extractor] Regex failed:", e)
    
        return list(keywords)[:15]
