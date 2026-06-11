import re


class GraphBuilder:
    """
    Extracts (subject, relation, object) triples from any text using
    pure regex/NLP — no predefined domain rules, no external libraries.

    Patterns covered:
      "X is a Y"        → (X, is_a, Y)
      "X is Y"          → (X, is, Y)
      "X are Y"         → (X, are, Y)
      "X has Y"         → (X, has, Y)
      "X can Y"         → (X, can, Y)
      "X uses Y"        → (X, uses, Y)
      "X belongs to Y"  → (X, belongs_to, Y)
      "X part of Y"     → (X, part_of, Y)
      "X related to Y"  → (X, related_to, Y)
      "X causes Y"      → (X, causes, Y)
      "X contains Y"    → (X, contains, Y)
      "X enables Y"     → (X, enables, Y)
      noun-pair fallback → (noun1, related_to, noun2)
    """

    # (pattern, relation_label, subject_group, object_group)
    _PATTERNS = [
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+is\s+a\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'is_a', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+are\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'are', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+is\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'is', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+has\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'has', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+can\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'can', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+uses?\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'uses', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+belongs\s+to\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'belongs_to', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+(?:is\s+)?part\s+of\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'part_of', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+(?:is\s+)?related\s+to\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'related_to', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+causes?\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'causes', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+contains?\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'contains', 1, 2),
        (r'\b([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\s+enables?\s+([A-Za-z][a-z]+(?:\s[A-Za-z][a-z]+)?)\b', 'enables', 1, 2),
    ]

    # words to skip as standalone nodes
    _STOP = {
        'the','a','an','is','are','was','were','be','been','being',
        'have','has','had','do','does','did','will','would','could',
        'should','may','might','shall','this','that','these','those',
        'it','its','we','they','he','she','you','i','my','our','their',
        'and','or','but','so','yet','for','nor','in','on','at','by',
        'to','of','with','from','as','into','through','about','than',
        'very','just','also','only','even','still','more','most','all',
        'some','any','each','every','both','few','many','much','more',
    }

    def _clean(self, text):
        return re.sub(r'[^\w\s]', '', text).strip()

    def _titled(self, text):
        return ' '.join(w.capitalize() for w in text.split())

    def _extract_nouns(self, text):
        """Rough noun extraction: capitalised words and words >4 chars not in stop list."""
        words = re.findall(r'\b[A-Za-z][a-z]{3,}\b', text)
        return [w for w in words if w.lower() not in self._STOP]

    def extract(self, text):
        relations = []
        seen = set()

        # Try structured patterns first
        for pattern, rel, sg, og in self._PATTERNS:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                subj = self._titled(self._clean(m.group(sg)))
                obj  = self._titled(self._clean(m.group(og)))
                if subj and obj and subj.lower() != obj.lower():
                    key = (subj, rel, obj)
                    if key not in seen:
                        seen.add(key)
                        relations.append(key)

        # Fallback: noun-pair co-occurrence within same sentence
        if not relations:
            sentences = re.split(r'[.!?]', text)
            for sent in sentences:
                nouns = self._extract_nouns(sent)
                nouns = list(dict.fromkeys(nouns))  # dedup preserving order
                for i in range(len(nouns) - 1):
                    n1 = self._titled(nouns[i])
                    n2 = self._titled(nouns[i + 1])
                    if n1 != n2:
                        key = (n1, 'related_to', n2)
                        if key not in seen:
                            seen.add(key)
                            relations.append(key)

        return relations
