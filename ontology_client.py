import os
from urllib.parse import urlsplit
import httpx

class OntologyUnavailable(RuntimeError):
    pass

def load_bundle(domain: str) -> dict:
    if domain not in ("bonds", "equities", "commodities"):
        raise ValueError("Invalid ontology selection")
    base = os.getenv("ONTOLOGY_BASE_URL", "").strip().rstrip("/")
    if not base:
        raise OntologyUnavailable("Missing ONTOLOGY_BASE_URL repository secret/variable")
    u = urlsplit(base)
    if u.scheme != "https" and not (u.scheme == "http" and u.hostname in {"127.0.0.1", "localhost"}):
        raise OntologyUnavailable("ONTOLOGY_BASE_URL must be HTTPS (or local HTTP for development)")
    try:
        response = httpx.get(f"{base}/bundle/{domain}", timeout=12, follow_redirects=False)
        response.raise_for_status()
        data = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise OntologyUnavailable(f"Cannot reach or parse ontology server: {exc}") from exc
    if not isinstance(data, dict) or data.get("selected_domain") != domain:
        raise OntologyUnavailable("Ontology server returned unexpected domain")
    for key in ("general", "domain"):
        o = data.get(key)
        if not isinstance(o, dict) or not isinstance(o.get("concepts"), list) or not isinstance(o.get("relationships"), list):
            raise OntologyUnavailable(f"Malformed {key} ontology")
    if data["general"].get("id") != "general" or data["domain"].get("id") != domain:
        raise OntologyUnavailable("Unexpected ontology identifier")
    return data
