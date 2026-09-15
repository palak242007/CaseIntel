```python
"""
CaseIntel - Case Correlation Module

Purpose:
    Identify potentially related cybercrime cases using:
        1. Shared cyber indicators
        2. TF-IDF cosine similarity between complaint texts
        3. Connected-component clustering using Union-Find

Input:
    data/extracted_indicators.json

Output:
    data/case_clusters.json

Important:
    Correlation results are investigation leads, NOT proof that
    two cases were committed by the same person or organization.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "extracted_indicators.json"
OUTPUT_FILE = BASE_DIR / "data" / "case_clusters.json"

# Minimum textual similarity required to create a text-based
# relationship.
TEXT_SIMILARITY_THRESHOLD = 0.55

# Minimum number of shared indicators required to create a
# relationship based on structured indicators.
MIN_SHARED_INDICATORS = 1

# Weight given to structured indicators and text similarity.
INDICATOR_WEIGHT = 0.70
TEXT_WEIGHT = 0.30


# ============================================================
# UNION-FIND / DISJOINT SET
# ============================================================

class UnionFind:
    """
    Union-Find data structure.

    Used to group related cases into connected components.

    Example:

        C001 <-> C002
        C002 <-> C003

    becomes:

        {C001, C002, C003}
    """

    def __init__(self, items: List[str]):
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item: str) -> str:
        """Return the root of an item."""
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])

        return self.parent[item]

    def union(self, first: str, second: str) -> None:
        """Join two sets."""
        root_first = self.find(first)
        root_second = self.find(second)

        if root_first == root_second:
            return

        if self.rank[root_first] < self.rank[root_second]:
            self.parent[root_first] = root_second

        elif self.rank[root_first] > self.rank[root_second]:
            self.parent[root_second] = root_first

        else:
            self.parent[root_second] = root_first
            self.rank[root_first] += 1


# ============================================================
# FILE HELPERS
# ============================================================

def load_json(file_path: Path) -> Any:
    """Load JSON from disk."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_path: Path, data: Any) -> None:
    """Save JSON to disk."""

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_value(value: Any) -> str:
    """
    Normalize an indicator before comparison.

    Example:

        ' 9876543210 ' -> '9876543210'
        'ABC@UPI'      -> 'abc@upi'
    """

    if value is None:
        return ""

    value = str(value).strip().lower()

    # Remove trailing punctuation.
    value = value.rstrip(".,;:")

    return value


def normalize_indicator_list(value: Any) -> List[str]:
    """
    Convert different possible JSON representations into
    a normalized list of strings.
    """

    if value is None:
        return []

    if isinstance(value, str):
        value = [value]

    if not isinstance(value, list):
        return []

    normalized = []

    for item in value:
        value_string = normalize_value(item)

        if value_string:
            normalized.append(value_string)

    return sorted(set(normalized))


# ============================================================
# CASE EXTRACTION
# ============================================================

def get_case_id(case: Dict[str, Any], index: int) -> str:
    """
    Extract case ID from several common field names.
    """

    possible_keys = [
        "case_id",
        "caseId",
        "id",
        "case"
    ]

    for key in possible_keys:
        if key in case and case[key]:
            return str(case[key])

    return f"C{index + 1:03d}"


def get_case_text(case: Dict[str, Any]) -> str:
    """
    Extract complaint/case text.

    Supports several common field names.
    """

    possible_keys = [
        "text",
        "complaint",
        "complaint_text",
        "description",
        "narrative",
        "case_text",
        "content"
    ]

    for key in possible_keys:
        value = case.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def extract_indicators(case: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Extract indicator categories from a case.

    Supported categories:
        - phone_numbers
        - upi_ids
        - urls
        - email_addresses
        - ip_addresses
        - account_numbers

    The function also accepts common alternative names.
    """

    aliases = {
        "phone_numbers": [
            "phone_numbers",
            "phones",
            "phone",
            "mobile_numbers",
            "mobile"
        ],

        "upi_ids": [
            "upi_ids",
            "upi",
            "upi_addresses"
        ],

        "urls": [
            "urls",
            "url",
            "links",
            "websites"
        ],

        "email_addresses": [
            "email_addresses",
            "emails",
            "email"
        ],

        "ip_addresses": [
            "ip_addresses",
            "ips",
            "ip"
        ],

        "account_numbers": [
            "account_numbers",
            "accounts",
            "bank_accounts"
        ]
    }

    indicators = {}

    # First look directly inside the case.
    for standard_name, possible_keys in aliases.items():

        values = []

        for key in possible_keys:
            if key in case:
                values.extend(
                    normalize_indicator_list(case[key])
                )

        indicators[standard_name] = sorted(set(values))

    # Also support a nested "indicators" object.
    nested = case.get("indicators")

    if isinstance(nested, dict):

        for standard_name, possible_keys in aliases.items():

            for key in possible_keys:

                if key in nested:
                    indicators[standard_name].extend(
                        normalize_indicator_list(
                            nested[key]
                        )
                    )

            indicators[standard_name] = sorted(
                set(indicators[standard_name])
            )

    return indicators


# ============================================================
# CASE PREPARATION
# ============================================================

def prepare_cases(raw_data: Any) -> List[Dict[str, Any]]:
    """
    Convert the input JSON into a standard internal format.
    """

    if isinstance(raw_data, list):
        raw_cases = raw_data

    elif isinstance(raw_data, dict):

        # Common structure:
        # {
        #   "cases": [...]
        # }
        if isinstance(raw_data.get("cases"), list):
            raw_cases = raw_data["cases"]

        # Alternative structure:
        # {
        #   "data": [...]
        # }
        elif isinstance(raw_data.get("data"), list):
            raw_cases = raw_data["data"]

        else:
            # If the JSON contains a single case.
            raw_cases = [raw_data]

    else:
        raise ValueError(
            "Unsupported input JSON format."
        )

    cases = []

    for index, raw_case in enumerate(raw_cases):

        if not isinstance(raw_case, dict):
            continue

        case_id = get_case_id(raw_case, index)
        text = get_case_text(raw_case)
        indicators = extract_indicators(raw_case)

        cases.append({
            "case_id": case_id,
            "text": text,
            "indicators": indicators
        })

    return cases


# ============================================================
# INDICATOR COMPARISON
# ============================================================

def get_shared_indicators(
    first: Dict[str, List[str]],
    second: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    """
    Return indicators shared by two cases.
    """

    shared = {}

    all_types = set(first.keys()) | set(second.keys())

    for indicator_type in all_types:

        first_values = set(
            first.get(indicator_type, [])
        )

        second_values = set(
            second.get(indicator_type, [])
        )

        overlap = sorted(
            first_values.intersection(second_values)
        )

        if overlap:
            shared[indicator_type] = overlap

    return shared


def count_shared_indicators(
    shared: Dict[str, List[str]]
) -> int:
    """Count total shared indicator values."""

    return sum(
        len(values)
        for values in shared.values()
    )


# ============================================================
# INDICATOR SCORING
# ============================================================

def calculate_indicator_score(
    shared: Dict[str, List[str]]
) -> float:
    """
    Calculate an indicator-based score.

    The score is capped at 1.0.

    Multiple indicator categories increase the score.
    """

    if not shared:
        return 0.0

    category_weights = {
        "phone_numbers": 0.40,
        "upi_ids": 0.35,
        "urls": 0.20,
        "email_addresses": 0.15,
        "ip_addresses": 0.20,
        "account_numbers": 0.25
    }

    score = 0.0

    for category in shared:

        score += category_weights.get(
            category,
            0.10
        )

    return min(score, 1.0)


# ============================================================
# TEXT SIMILARITY
# ============================================================

def clean_text(text: str) -> str:
    """Basic text normalization for TF-IDF."""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = re.sub(
        r"[^\w\s@./:-]",
        " ",
        text
    )

    return text.strip()


def calculate_text_similarities(
    cases: List[Dict[str, Any]]
) -> Dict[Tuple[str, str], float]:
    """
    Calculate pairwise TF-IDF cosine similarity.

    Returns:
        {
            ("C001", "C002"): 0.81,
            ("C001", "C003"): 0.21
        }
    """

    similarities = {}

    if not SKLEARN_AVAILABLE:
        return similarities

    if len(cases) < 2:
        return similarities

    documents = [
        clean_text(case["text"])
        for case in cases
    ]

    # If no case has usable text, skip TF-IDF.
    if not any(documents):
        return similarities

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(
            documents
        )

        similarity_matrix = cosine_similarity(
            matrix
        )

    except ValueError:
        return similarities

    for i in range(len(cases)):

        for j in range(i + 1, len(cases)):

            first_id = cases[i]["case_id"]
            second_id = cases[j]["case_id"]

            score = float(
                similarity_matrix[i][j]
            )

            similarities[
                (first_id, second_id)
            ] = round(score, 4)

    return similarities


# ============================================================
# RELATIONSHIP CREATION
# ============================================================

def determine_relationship_type(
    indicator_score: float,
    text_score: float,
    shared_count: int
) -> Tuple[bool, str, float]:
    """
    Determine whether two cases should be connected.

    Structured indicators have priority over text similarity.

    Returns:
        should_link
        relationship_type
        combined_score
    """

    indicator_match = (
        shared_count >= MIN_SHARED_INDICATORS
    )

    text_match = (
        text_score >= TEXT_SIMILARITY_THRESHOLD
    )

    combined_score = (
        indicator_score * INDICATOR_WEIGHT
        + text_score * TEXT_WEIGHT
    )

    # Strong relationship:
    # multiple indicators OR a high indicator score.
    if indicator_match and (
        shared_count >= 2
        or indicator_score >= 0.50
    ):
        return (
            True,
            "strong",
            round(max(combined_score, indicator_score), 4)
        )

    # Moderate relationship:
    # at least one indicator.
    if indicator_match:
        return (
            True,
            "moderate",
            round(max(combined_score, indicator_score), 4)
        )

    # Text-only relationship.
    if text_match:
        return (
            True,
            "weak",
            round(combined_score, 4)
        )

    return (
        False,
        "none",
        round(combined_score, 4)
    )


# ============================================================
# RELATIONSHIP REASONS
# ============================================================

def build_relationship_reasons(
    shared: Dict[str, List[str]],
    text_score: float
) -> List[str]:

    reasons = []

    reason_names = {
        "phone_numbers":
            "Same phone number appears in both cases",

        "upi_ids":
            "Same UPI ID appears in both cases",

        "urls":
            "Same URL appears in both cases",

        "email_addresses":
            "Same email address appears in both cases",

        "ip_addresses":
            "Same IP address appears in both cases",

        "account_numbers":
            "Same account number appears in both cases"
    }

    for indicator_type in shared:

        reasons.append(
            reason_names.get(
                indicator_type,
                f"Shared {indicator_type} detected"
            )
        )

    if text_score >= TEXT_SIMILARITY_THRESHOLD:

        reasons.append(
            "Complaint text shows significant similarity"
        )

    return reasons


# ============================================================
# PAIRWISE CORRELATION
# ============================================================

def correlate_cases(
    cases: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], UnionFind]:

    case_ids = [
        case["case_id"]
        for case in cases
    ]

    union_find = UnionFind(case_ids)

    relationships = []

    text_similarities = calculate_text_similarities(
        cases
    )

    for i in range(len(cases)):

        for j in range(i + 1, len(cases)):

            first = cases[i]
            second = cases[j]

            first_id = first["case_id"]
            second_id = second["case_id"]

            shared = get_shared_indicators(
                first["indicators"],
                second["indicators"]
            )

            shared_count = count_shared_indicators(
                shared
            )

            indicator_score = calculate_indicator_score(
                shared
            )

            text_score = text_similarities.get(
                (first_id, second_id),
                0.0
            )

            should_link, relationship_type, score = (
                determine_relationship_type(
                    indicator_score,
                    text_score,
                    shared_count
                )
            )

            if not should_link:
                continue

            union_find.union(
                first_id,
                second_id
            )

            relationships.append({
                "case_1": first_id,
                "case_2": second_id,
                "relationship_type": relationship_type,
                "correlation_score": score,
                "indicator_score": round(
                    indicator_score,
                    4
                ),
                "text_similarity": round(
                    text_score,
                    4
                ),
                "shared_indicators": shared,
                "relationship_reasons":
                    build_relationship_reasons(
                        shared,
                        text_score
                    ),
                "investigation_lead": True,
                "requires_human_verification": True
            })

    return relationships, union_find


# ============================================================
# CLUSTER CREATION
# ============================================================

def create_clusters(
    cases: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
    union_find: UnionFind
) -> Tuple[List[Dict[str, Any]], List[str]]:

    grouped = {}

    for case in cases:

        case_id = case["case_id"]

        root = union_find.find(case_id)

        grouped.setdefault(
            root,
            []
        ).append(case_id)

    # Only groups containing at least two cases are clusters.
    cluster_groups = [
        group
        for group in grouped.values()
        if len(group) >= 2
    ]

    clustered_case_ids = set()

    clusters = []

    for index, case_ids in enumerate(
        sorted(
            cluster_groups,
            key=lambda x: sorted(x)
        ),
        start=1
    ):

        cluster_id = f"CL{index:03d}"

        case_ids = sorted(case_ids)

        clustered_case_ids.update(
            case_ids
        )

        cluster_relationships = [
            relationship
            for relationship in relationships
            if (
                relationship["case_1"] in case_ids
                and
                relationship["case_2"] in case_ids
            )
        ]

        shared_by_type: Dict[str, Set[str]] = {}

        for relationship in cluster_relationships:

            for indicator_type, values in (
                relationship["shared_indicators"].items()
            ):

                shared_by_type.setdefault(
                    indicator_type,
                    set()
                )

                shared_by_type[
                    indicator_type
                ].update(values)

        shared_indicators = {
            indicator_type: sorted(values)
            for indicator_type, values
            in shared_by_type.items()
        }

        scores = [
            relationship["correlation_score"]
            for relationship
            in cluster_relationships
        ]

        if scores:
            cluster_score = round(
                max(scores),
                4
            )
        else:
            cluster_score = 0.0

        relationship_types = [
            relationship["relationship_type"]
            for relationship
            in cluster_relationships
        ]

        if "strong" in relationship_types:
            relationship_type = "strong"

        elif "moderate" in relationship_types:
            relationship_type = "moderate"

        else:
            relationship_type = "weak"

        reasons = []

        for relationship in cluster_relationships:

            for reason in relationship[
                "relationship_reasons"
            ]:

                if reason not in reasons:
                    reasons.append(reason)

        if relationship_type == "strong":
            confidence = "high"

        elif relationship_type == "moderate":
            confidence = "medium"

        else:
            confidence = "low"

        clusters.append({
            "cluster_id": cluster_id,
            "case_ids": case_ids,
            "relationship_type": relationship_type,
            "correlation_score": cluster_score,
            "shared_indicators": shared_indicators,
            "relationship_reasons": reasons,
            "relationship_count": len(
                cluster_relationships
            ),
            "investigation_lead": True,
            "confidence": confidence,
            "requires_human_verification": True
        })

    all_case_ids = {
        case["case_id"]
        for case in cases
    }

    unclustered_cases = sorted(
        all_case_ids - clustered_case_ids
    )

    return clusters, unclustered_cases


# ============================================================
# OUTPUT GENERATION
# ============================================================

def build_output(
    cases: List[Dict[str, Any]],
    relationships: List[Dict[str, Any]],
    clusters: List[Dict[str, Any]],
    unclustered_cases: List[str]
) -> Dict[str, Any]:

    return {
        "clusters": clusters,

        "relationships": relationships,

        "unclustered_cases": unclustered_cases,

        "metadata": {
            "total_cases": len(cases),
            "total_clusters": len(clusters),
            "total_clustered_cases": sum(
                len(cluster["case_ids"])
                for cluster in clusters
            ),
            "total_unclustered_cases":
                len(unclustered_cases),

            "total_relationships":
                len(relationships),

            "correlation_method": [
                "shared_indicators",
                "tfidf_cosine_similarity",
                "connected_component_clustering"
            ],

            "indicator_types": [
                "phone_numbers",
                "upi_ids",
                "urls",
                "email_addresses",
                "ip_addresses",
                "account_numbers"
            ],

            "text_similarity_threshold":
                TEXT_SIMILARITY_THRESHOLD,

            "minimum_shared_indicators":
                MIN_SHARED_INDICATORS,

            "indicator_weight":
                INDICATOR_WEIGHT,

            "text_weight":
                TEXT_WEIGHT,

            "sklearn_available":
                SKLEARN_AVAILABLE,

            "purpose":
                "Identify potentially related cybercrime cases "
                "and generate investigation leads for human verification.",

            "warning":
                "Correlation does not establish that cases were "
                "committed by the same person or organization."
        }
    }


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_correlation(
    input_file: Path = INPUT_FILE,
    output_file: Path = OUTPUT_FILE
) -> Dict[str, Any]:

    print("=" * 60)
    print("CaseIntel - Case Correlation Module")
    print("=" * 60)

    print(f"\nInput : {input_file}")
    print(f"Output: {output_file}")

    # --------------------------------------------------------
    # 1. Load input
    # --------------------------------------------------------

    print("\n[1/5] Loading extracted indicators...")

    raw_data = load_json(
        input_file
    )

    # --------------------------------------------------------
    # 2. Prepare cases
    # --------------------------------------------------------

    print("[2/5] Preparing cases...")

    cases = prepare_cases(
        raw_data
    )

    if not cases:
        raise ValueError(
            "No valid cases found in input file."
        )

    print(
        f"      Loaded {len(cases)} cases."
    )

    # --------------------------------------------------------
    # 3. Correlate
    # --------------------------------------------------------

    print(
        "[3/5] Comparing cases..."
    )

    relationships, union_find = correlate_cases(
        cases
    )

    print(
        f"      Found {len(relationships)} "
        f"potential relationships."
    )

    # --------------------------------------------------------
    # 4. Build clusters
    # --------------------------------------------------------

    print(
        "[4/5] Building case clusters..."
    )

    clusters, unclustered_cases = create_clusters(
        cases,
        relationships,
        union_find
    )

    print(
        f"      Created {len(clusters)} clusters."
    )

    print(
        f"      Unclustered cases: "
        f"{len(unclustered_cases)}"
    )

    # --------------------------------------------------------
    # 5. Save output
    # --------------------------------------------------------

    print(
        "[5/5] Saving results..."
    )

    output = build_output(
        cases,
        relationships,
        clusters,
        unclustered_cases
    )

    save_json(
        output_file,
        output
    )

    print(
        f"\nSaved successfully to:"
        f"\n{output_file}"
    )

    print("\n" + "=" * 60)
    print("Correlation completed successfully.")
    print("=" * 60)

    return output


# ============================================================
# COMMAND-LINE ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        run_correlation()

    except FileNotFoundError as error:

        print(
            f"\nERROR: {error}"
        )

        print(
            "\nMake sure the following file exists:"
        )

        print(
            f"  {INPUT_FILE}"
        )

    except json.JSONDecodeError as error:

        print(
            "\nERROR: Invalid JSON input."
        )

        print(
            f"Details: {error}"
        )

    except Exception as error:

        print(
            "\nERROR: Correlation failed."
        )

        print(
            f"Details: {error}"
        )
```

### Install dependency

This module uses scikit-learn for TF-IDF and cosine similarity:

```bash
pip install scikit-learn
```

Then run:

```bash
python modules/correlation/correlate.py
```

It should produce:

```text
data/
└── case_clusters.json
```

The important design choice here is that **shared indicators are treated as structured evidence and text similarity as a supporting signal**. The output explicitly marks relationships as investigation leads requiring human verification, rather than treating correlation as proof.
