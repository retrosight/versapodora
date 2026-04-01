from datetime import datetime

def parse_date(date_str):
    """Parse various date formats and return ISO8601 YYYY-MM-DD string."""
    date_str = date_str.strip()
    
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",  # 2025-01-02T06:25:08Z
        "%Y-%m-%d",             # 2025-06-25
        "%m/%d/%Y",             # 01/02/2025, 08/25/2025
        "%m/%d/%y",             # 02/13/26
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")


dates = [
    "2025-01-02T06:25:08Z",
    "01/02/2025",
    "08/25/2025",
    "02/13/26",
    "03/20/2025",
    "12/04/2025",
    "12/28/2025",
    "12/27/2025",
    "3/6/2025",
    "8/1/2025",
    "06/10/2025",
    "2025-06-25",
    "1-1-2021"
]

for date in dates:
    print(f"{date:30s} → {parse_date(date)}")
