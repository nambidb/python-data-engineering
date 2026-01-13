import os
import re
import time
import logging
import requests
import csv
from dotenv import load_dotenv

#Setup
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
FAILED_CSV   = "data_files/failed_companies.csv"

#Structured_Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("company_enrichment")

#Company_ID Regex Validation
COMPANY_ID_REGEX = re.compile(r"^\d{8}$")

def normalize_company_id(raw_id):
    if not raw_id or not isinstance(raw_id, str):
        return None, "null_or_nonstring"

    cleaned = raw_id.strip()
    if not cleaned.isdigit():
        return None, "non_numeric"

    normalized = cleaned.zfill(8)
    if not COMPANY_ID_REGEX.match(normalized):
        return None, "invalid_format"

    return normalized, None


def enrich_company(company_number):
    url = f"{BASE_URL}/{company_number}"

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
        logger.warning(f"Rate limit hit for {company_number}, retrying after {retry_after}s")
        time.sleep(retry_after)
        return enrich_company(company_number)

    else:
        return None, f"api_error_{response.status_code}"

#Main Pipeline
def main():
    logger.info("Starting company enrichment...")

    #Normalize & validate
    cleaned_ids = []
    failures = []

    for raw_id in RAW_COMPANY_IDS:
        normalized, reason = normalize_company_id(raw_id)
        if normalized:
            cleaned_ids.append(normalized)
        else:
            failures.append({"company_id": raw_id, "reason": reason})
            logger.warning(f"Skipped invalid input: {raw_id}, reason: {reason}")

    #Deduplicate
    unique_ids = list(set(cleaned_ids))
    logger.info(f"Raw count: {len(RAW_COMPANY_IDS)}, Cleaned count: {len(cleaned_ids)}, Unique count: {len(unique_ids)}")

    #Enrich
    results = []
    start_time = time.time()

    for idx, company_id in enumerate(unique_ids, start=1):
        record_start = time.time()
        logger.info(f"Enriching company ({idx}/{len(unique_ids)}): {company_id}")

        profile, error = enrich_company(company_id)
        if profile:
            results.append(profile)
        else:
            failures.append({"company_id": company_id, "reason": error})
            logger.warning(f"Failed to enrich {company_id}, reason: {error}")
        #time.sleep(0.5)
        # Timing info
        record_end = time.time()
        elapsed = record_end - record_start
        total_elapsed = record_end - start_time
        logger.info(f"Processed {company_id} in {elapsed:.2f}s, total elapsed: {total_elapsed:.2f}s")

    logger.info(f"Enrichment complete. Requested: {len(unique_ids)}, Successful: {len(results)}, Failed: {len(failures)}, Total time: {time.time() - start_time:.2f}s")

    #Save to CSV
    def write_to_csv(filepath, rows, fieldnames=None):
        if not rows:
            logger.info(f"No data to write for {filepath}")
            return

        if fieldnames is None:
            fieldnames = list(rows[0].keys())

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        logger.info(f"Wrote {len(rows)} records to {filepath}")

    write_to_csv(ENRICHED_CSV, results)
    write_to_csv(FAILED_CSV, failures, fieldnames=["company_id", "reason"])

    return results, failures

#Execution
if __name__ == "__main__":
    enriched, failed = main()

    print("\n--- Enriched Records ---")
    for record in enriched:
        print(record)

    print("\n--- Failed Records ---")
    for f in failed:
        print(f)
