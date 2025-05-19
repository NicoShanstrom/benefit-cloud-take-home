# benefit-cloud-take-home
take home python api project for benefit cloud solutions engineer role

# iChooseRx Google Sheets Export Tool

This is a CLI-based Python tool that pulls filtered drug data from the public iChooseRx API, performs data transformation, and writes the results to a Google Sheet using the Google Sheets API. It is designed for extensibility and follows a clean class-based architecture.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nicoshanstrom/benefit-cloud-take-home-project.git
cd benefit-cloud-take-home-project
```

### 2. Create & Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root and add the following line:

```env
GOOGLE_CREDENTIALS_PATH=credentials/service_account.json
```

Make sure your service account JSON credentials are saved at that path and that the target Google Sheet is shared with the service account email.

---

## 🧪 Usage

```bash
python src/main.py --drug-names Dextroamphetamine Lisdexamfetamine --filters artificial_colors preservatives
```

### Parameters

- `--drug-names` (required): One or more generic drug names or active ingredients.
- `--filters` (optional): Any combination of the following iChooseRx filter keys:

  ```
  artificial_colors
  artificial_sweeteners
  artificial_flavors
  preservatives
  gluten
  added_sugar
  vegan
  possible_endocrine_disruptors
  sugar_alcohols
  potentially_harmful_additives
  ```

---

## 🛠 Transformations Performed

- The tool filters drug variants based on the user's selected ingredients/excipients to avoid.
- It lists the drugs by filtered results in descending order for a user to see which drug has more filtered results.
- It calculates an **Alignment Score (0–10)** for each drug, reflecting how well its available versions match the selected filters.
- For each drug, it counts and lists in descending order the **top manufacturers** whose variants align with the filters.
- The output is formatted into a clean, timestamped report in Google Sheets with clearly structured metadata, summaries, and breakdowns.

---

## 📚 Architecture Overview

This project is built with extensibility and modularity in mind:

- `BaseAPIClient`: A reusable base class that handles HTTP interactions with any REST API.
- `IChooseRxAPI`: A specific subclass that interacts with the iChooseRx public export summaries endpoint.
- `GoogleSheetsExporter`: Handles authentication and writing structured data to new worksheets.
- Utility modules like `alignment_score.py`, `timestamp.py`, and `manufacturer_utils.py` encapsulate small, testable units of logic.
- The transformation logic is centralized in `summary_builder.py`, and the CLI lives in `main.py`.

This structure allows other APIs to be plugged in easily — you could subclass `BaseAPIClient` to support any public API (e.g. weather, crypto, or FDA data), swap out the transformation logic, and reuse the export pipeline.
