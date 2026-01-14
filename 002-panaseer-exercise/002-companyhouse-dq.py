import os
import re
import time
import logging
import requests
import pandas as pd
from dotenv import load_dotenv
from typing import List, Dict, Tuple, Optional

#API Setup
load_dotenv()
API_KEY = os.getenv("COMPANIES_HOUSE_API_KEY")
BASE_URL = "https://api.company-information.service.gov.uk/company"

RAW_COMPANY_IDS = [
    '00445790',      # Valid: Tesco
    '00002065',      # Valid
    '00445790',      # Duplicate
    ' 11563248 ',    # Dirty whitespace
    'INVALID_ID',    # Invalid format
    None,            # Null
    '00999999',      # Valid format but missing (404)
    '2065',          # Malformed (Excel-style missing zeros)
    '1000',
    '232323',
    '00.445790',
    '09098199',
    '1.15632E+07'
]

ENRICHED_CSV = "data_files/enriched_companies.csv"
FAILED_CSV = "data_files/failed_companies.csv"

# Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("company_enrichment")

COMPANY_ID_REGEX = re.compile(r"^\d{8}$")

#Normalize and Process IDs
def normalize_and_process_ids(raw_ids: List[Optional[str]]) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Normalize, validate, and deduplicate a list of raw company IDs.

    Handles dirty strings, Excel floats/scientific notation, whitespace, duplicates.

    Args:
        raw_ids (List[Optional[str]]): List of raw company IDs.

    Returns:
        Tuple[List[str], List[Dict[str, str]]]:
            - List of unique normalized 8-digit IDs
            - List of failed IDs with reason
    """
    cleaned_ids = []
    failures = []

    for raw_id in raw_ids:
        if not raw_id or not isinstance(raw_id, str):
            failures.append({"company_id": raw_id, "reason": "null_or_nonstring"})
            logger.warning(f"Skipped invalid input: {raw_id}, reason: null_or_nonstring")
            continue

        cleaned = raw_id.strip()

        if not cleaned.isdigit():
            failures.append({"company_id": raw_id, "reason": "non_numeric"})
            logger.warning(f"Skipped invalid input: {raw_id}, reason: non_numeric")
            continue

        normalized = cleaned.zfill(8)
        if not COMPANY_ID_REGEX.match(normalized):
            failures.append({"company_id": raw_id, "reason": "invalid_format"})
            logger.warning(f"Skipped invalid input: {raw_id}, reason: invalid_format")
            continue

        cleaned_ids.append(normalized)

    # Deduplicate
    unique_ids = list(set(cleaned_ids))
    logger.info(f"Raw count: {len(raw_ids)}, Cleaned count: {len(cleaned_ids)}, Unique count: {len(unique_ids)}")

    return unique_ids, failures

def enrich_companies(company_ids: List[str]) -> Tuple[List[Dict], List[Dict]]:
    """
    Enrich a list of company IDs by fetching details from Companies House API.

    Handles single ID enrichment, rate limiting, errors, and returns both successes and failures.

    Args:
        company_ids (List[str]): List of normalized 8-digit company IDs.

    Returns:
        Tuple[List[Dict], List[Dict]]:
            - List of successful company records
            - List of failed records with reason
    """
    results: List[Dict] = []
    failures: List[Dict[str, str]] = []
    start_time = time.time()

    for idx, company_id in enumerate(company_ids, start=1):
        record_start = time.time()
        logger.info(f"Enriching company ({idx}/{len(company_ids)}): {company_id}")

        # Inner function to fetch one company
        def fetch_company(c_id: str) -> Tuple[Optional[Dict], Optional[str]]:
            url = f"{BASE_URL}/{c_id}"
            try:
                response = requests.get(url, auth=(API_KEY, ""))
            except requests.RequestException as e:
                return None, f"request_exception: {e}"

            if response.status_code == 200:
                data = response.json()
                last_accounts = data.get("accounts", {}).get("last_accounts", {})
                return {
                    "company_number": data.get("company_number"),
                    "company_name": data.get("company_name"),
                    "company_status": data.get("company_status"),
                    "date_of_creation": data.get("date_of_creation"),
                    "date_of_cessation": data.get("date_of_cessation"),
                    "sic_codes": ",".join(data.get("sic_codes", [])),
                    "last_accounts_made_up_to": last_accounts.get("made_up_to"),
                    "last_accounts_type": last_accounts.get("type")
                }, None
            elif response.status_code == 404:
                return None, "404_not_found"
            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 10))
                logger.warning(f"Rate limit hit for {c_id}, retrying after {retry_after}s")
                time.sleep(retry_after)
                return fetch_company(c_id)
            else:
                return None, f"api_error_{response.status_code}"

        # Fetch the company
        profile, error = fetch_company(company_id)
        if profile:
            results.append(profile)
        else:
            failures.append({"company_id": company_id, "reason": error})
            logger.warning(f"Failed to enrich {company_id}, reason: {error}")

        record_end = time.time()
        elapsed = record_end - record_start
        total_elapsed = record_end - start_time
        logger.info(f"Processed {company_id} in {elapsed:.2f}s, total elapsed: {total_elapsed:.2f}s")

    return results, failures

def save_dataframe(df: pd.DataFrame, filepath: str) -> None:
    """
    Save a DataFrame to CSV and create directories if they don't exist.

    Args:
        df (pd.DataFrame): DataFrame to save.
        filepath (str): CSV file path.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False, encoding="utf-8")
    logger.info(f"Wrote {len(df)} records to {filepath}")

#Main Pipeline
def main() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main pipeline: normalize, deduplicate, enrich company IDs, and save results to CSV using pandas.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - DataFrame of successfully enriched company records
            - DataFrame of failed company records with reasons
    """
    unique_ids, normalize_failures  = normalize_and_process_ids(RAW_COMPANY_IDS)
    enriched, enrich_failures  = enrich_companies(unique_ids)

    all_failures = normalize_failures + enrich_failures

    enriched_df = pd.DataFrame(enriched)
    failed_df = pd.DataFrame(all_failures)

    save_dataframe(enriched_df, ENRICHED_CSV)
    save_dataframe(failed_df, FAILED_CSV)

    return enriched_df, failed_df

#Execution
if __name__ == "__main__":
    enriched_df, failed_df = main()

    print("\n--- Enriched Records ---")
    print(enriched_df)

    print("\n--- Failed Records ---")
    print(failed_df)