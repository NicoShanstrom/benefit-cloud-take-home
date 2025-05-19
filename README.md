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

## 🔍 Example API Response

This is a sample of the JSON data returned by the iChooseRx export summaries endpoint when queried with:

```http
GET /api/v1/export_summaries?drug_names[]=dextroamphetamine&drug_names[]=lisdexamfetamine&filters[]=artificial_colors&filters[]=preservatives
```
```
{
    "filters_applied": [
        {
            "key": "artificial_colors",
            "label": "Artificial Colors"
        },
        {
            "key": "preservatives",
            "label": "Preservatives"
        }
    ],
    "summary": [
        {
            "id": "dextroamphetamine",
            "type": "drug_summary",
            "attributes": {
                "drug_name": "dextroamphetamine",
                "total_results": 117,
                "filtered_results": 11,
                "variants": [
                    {
                        "brand_name": "DEXTROAMPHETAMINE SACCHARATE, AMPHETAMINE ASPARTATE, DEXTROAMPHETAMINE SULFATE, AND AMPHETAMINE SULFATE",
                        "manufacturer_name": "Ascent Pharmaceuticals, Inc.",
                        "product_ndc": "43602-982"
                    },
                    {
                        "brand_name": "XELSTRYM",
                        "manufacturer_name": "Noven Therapeutics, LLC",
                        "product_ndc": "68968-0205"
                    },
                    {
                        "brand_name": "DEXTROAMPHETAMINE SACCHARATE, AMPHETAMINE ASPARTATE, DEXTROAMPHETAMINE SULFATE, AND AMPHETAMINE SULFATE",
                        "manufacturer_name": "Camber Pharmaceuticals, Inc.",
                        "product_ndc": "31722-155"
                    },
                    {
                        "brand_name": "Dextroamphetamine Saccharate, Amphetamine Aspartate, Dextroamphetamine Sulfate, Amphetamine Sulfate",
                        "manufacturer_name": "GLENMARK PHARMACEUTICALS INC., USA",
                        "product_ndc": "68462-647"
                    },
                    {
                        "brand_name": "DEXTROAMPHETAMINE SACCHARATE, AMPHETAMINE ASPARTATE, DEXTROAMPHETAMINE SULFATE, AND AMPHETAMINE SULFATE",
                        "manufacturer_name": "Ascent Pharmaceuticals, Inc",
                        "product_ndc": "43602-370"
                    },
                    {
                        "brand_name": "Dextroamphetamine Saccharate and Amphetamine Aspartate and Dextroamphetamine Sulfate and Amphetamine Sulfate",
                        "manufacturer_name": "SpecGx LLC",
                        "product_ndc": "0406-8884"
                    },
                    {
                        "brand_name": "Dextroamphetamine Saccharate, Amphetamine Aspartate, Dextroamphetamine Sulfate and Amphetamine Sulfate",
                        "manufacturer_name": "Granules Pharmaceuticals Inc.",
                        "product_ndc": "70010-111"
                    },
                    {
                        "brand_name": "Dextroamphetamine Saccharate, Amphetamine Aspartate, Dextroamphetamine Sulfate, Amphetamine Sulfate Tablets,CII",
                        "manufacturer_name": "Alvogen Inc.",
                        "product_ndc": "47781-174"
                    },
                    {
                        "brand_name": "Dextroamphetamine Saccharate, Amphetamine Aspartate, Dextroamphetamine Sulfate, Amphetamine Sulfate",
                        "manufacturer_name": "Neolpharma, Inc.",
                        "product_ndc": "55466-129"
                    },
                    {
                        "brand_name": "DEXTROAMPHETAMINE SULFATE",
                        "manufacturer_name": "SpecGx LLC",
                        "product_ndc": "0406-8958"
                    },
                    {
                        "brand_name": "Adderall",
                        "manufacturer_name": "Teva Pharmaceuticals USA, Inc.",
                        "product_ndc": "57844-105"
                    }
                ]
            }
        },
        {
            "id": "lisdexamfetamine",
            "type": "drug_summary",
            "attributes": {
                "drug_name": "lisdexamfetamine",
                "total_results": 30,
                "filtered_results": 4,
                "variants": [
                    {
                        "brand_name": "Lisdexamfetamine Dimesylate",
                        "manufacturer_name": "SpecGx LLC",
                        "product_ndc": "0406-5124"
                    },
                    {
                        "brand_name": "Lisdexamfetamine dimesylate",
                        "manufacturer_name": "Novadoz Pharmaceuticals LLC",
                        "product_ndc": "72205-132"
                    },
                    {
                        "brand_name": "lisdexamfetamine dimesylate",
                        "manufacturer_name": "Teva Pharmaceuticals, Inc.",
                        "product_ndc": "0480-9737"
                    },
                    {
                        "brand_name": "Lisdexamfetamine dimesylate",
                        "manufacturer_name": "Granules Pharmaceuticals Inc.",
                        "product_ndc": "70010-214"
                    }
                ]
            }
        }
    ]
}
```

## 🧪 Usage (CLI input in Terminal)

```bash
python src/main.py --drug-names Dextroamphetamine Lisdexamfetamine --filters artificial_colors preservatives
```
`python src/main.py --help` to output all the available arguments, their descriptions, and usage examples. 

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

This project is designed with modularity and reusability in mind:

- `BaseAPIClient`: A reusable base class that handles HTTP interactions with any RESTful API, abstracting request logic for consistency across integrations.
- `IChooseRxAPI`: A specific subclass of `BaseAPIClient` that connects to the iChooseRx public export summaries endpoint and provides a method for fetching drug data with user-selected filters.
- `GoogleSheetsExporter`: Manages authentication with the Google Sheets API and writes structured rows of data to a new worksheet.
- Utility modules:
  - `alignment_score.py`: Calculates a normalized alignment score (0–10) based on how well a drug's variants match selected filters.
  - `manufacturer_utils.py`: Tallies manufacturers present in filtered results.
  - `timestamp.py`: Generates clean, sheet-safe UTC timestamps for logging and naming.
- `summary_builder.py`: Transforms raw API data into a clean, export-ready format while preserving user metadata (timestamp, filters used) and enriching it with sorted manufacturer counts and drugs based on filtered results.
- `main.py`: Acts as the CLI entry point. It handles argument parsing, orchestrates data fetching and transformation, and triggers export to Google Sheets.

➡️ To adapt this project for another API, simply:
1. Create a new subclass of `BaseAPIClient`.
2. Implement a corresponding transformation function (like `summary_builder.py`).
3. Update the CLI (`main.py`) to reflect the new API’s parameters.

The rest of the pipeline — data export, formatting logic, and modular utilities — can be reused as-is.