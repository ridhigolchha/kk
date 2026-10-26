import argparse
import csv
import json
import random
from typing import Iterable, List, TextIO


class LeadGenerator:
    """Generate and score leads for outbound sales and B2B growth campaigns."""

    INDUSTRIES = {
        "saas": 20,
        "software": 18,
        "healthcare": 15,
        "fintech": 16,
        "ecommerce": 14,
        "manufacturing": 12,
        "professional services": 10,
    }

    JOB_KEYWORDS = {
        "chief": 18,
        "vp": 18,
        "director": 16,
        "head": 16,
        "manager": 12,
        "owner": 14,
        "founder": 15,
    }

    PAIN_KEYWORDS = {
        "pipeline": 15,
        "lead conversion": 15,
        "revenue": 18,
        "growth": 12,
        "manual follow-up": 12,
        "sales efficiency": 16,
        "crm": 10,
        "retention": 10,
        "customer acquisition": 14,
    }

    SOURCE_WEIGHTS = {
        "outbound": 10,
        "referral": 14,
        "networking": 12,
        "website": 8,
        "ads": 9,
        "event": 11,
    }

    TEMPLATE_LEADS = [
        {
            "company": "Northwind Analytics",
            "industry": "SaaS",
            "job_title": "VP of Revenue",
            "email": "vp@northwindanalytics.com",
            "budget": 50000,
            "source": "Outbound",
            "pain_points": ["pipeline growth", "lead conversion"],
        },
        {
            "company": "Summit Health Group",
            "industry": "Healthcare",
            "job_title": "Operations Director",
            "email": "ops@summithealthgroup.com",
            "budget": 42000,
            "source": "Referral",
            "pain_points": ["manual follow-up", "patient acquisition"],
        },
        {
            "company": "Elevation Labs",
            "industry": "Fintech",
            "job_title": "Head of Growth",
            "email": "growth@elevationlabs.io",
            "budget": 75000,
            "source": "Networking",
            "pain_points": ["revenue growth", "lead conversion"],
        },
        {
            "company": "Forge Commerce",
            "industry": "Ecommerce",
            "job_title": "Marketing Manager",
            "email": "marketing@forgecommerce.com",
            "budget": 31000,
            "source": "Website",
            "pain_points": ["sales efficiency", "CRM cleanup"],
        },
        {
            "company": "Bluepeak Manufacturing",
            "industry": "Manufacturing",
            "job_title": "Operations Owner",
            "email": "owner@bluepeakmfg.com",
            "budget": 68000,
            "source": "Event",
            "pain_points": ["customer acquisition", "pipeline quality"],
        },
    ]

    def score_lead(self, lead: dict) -> int:
        """Return a score between 0 and 100 based on fit, intent, and buying readiness."""
        score = 0

        industry = str(lead.get("industry", "")).lower()
        job_title = str(lead.get("job_title", "")).lower()
        source = str(lead.get("source", "")).lower()
        budget = lead.get("budget", 0) or 0
        pain_points = [str(item).lower() for item in lead.get("pain_points", [])]

        if industry in self.INDUSTRIES:
            score += self.INDUSTRIES[industry]
        else:
            for keyword, value in self.INDUSTRIES.items():
                if keyword in industry:
                    score += value
                    break

        if any(keyword in job_title for keyword in self.JOB_KEYWORDS):
            for keyword, value in self.JOB_KEYWORDS.items():
                if keyword in job_title:
                    score += value
                    break
        elif job_title:
            score += 5

        if budget >= 25000:
            score += 20
        elif budget >= 10000:
            score += 10

        if source in self.SOURCE_WEIGHTS:
            score += self.SOURCE_WEIGHTS[source]

        if pain_points:
            score += min(25, len(pain_points) * 8)
            for pain in pain_points:
                for keyword, value in self.PAIN_KEYWORDS.items():
                    if keyword in pain:
                        score += value
                        break

        if lead.get("company"):
            score += 5

        return max(0, min(100, score))

    def generate_batch(self, count: int = 5) -> List[dict]:
        """Generate a list of synthetic leads with a lead score attached."""
        generated: List[dict] = []
        for _ in range(max(1, int(count))):
            template = random.choice(self.TEMPLATE_LEADS).copy()
            template["company"] = f"{template['company']} {random.randint(1, 99)}" if random.random() < 0.5 else template["company"]
            template["email"] = template["email"].replace("@", f"+{random.randint(10, 99)}@") if random.random() < 0.5 else template["email"]
            template["score"] = self.score_lead(template)
            generated.append(template)
        return generated

    def export_csv(self, leads: Iterable[dict], output: TextIO) -> TextIO:
        """Write leads to CSV using a normalized schema."""
        fieldnames = [
            "company",
            "industry",
            "job_title",
            "email",
            "budget",
            "source",
            "pain_points",
            "score",
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for lead in leads:
            row = {
                "company": lead.get("company", ""),
                "industry": lead.get("industry", ""),
                "job_title": lead.get("job_title", ""),
                "email": lead.get("email", ""),
                "budget": lead.get("budget", 0),
                "source": lead.get("source", ""),
                "pain_points": "; ".join(str(item) for item in lead.get("pain_points", [])),
                "score": lead.get("score", self.score_lead(lead)),
            }
            writer.writerow(row)

        return output


def _format_leads(leads: List[dict]) -> str:
    rows = []
    for lead in leads:
        rows.append(
            f"{lead.get('company', 'Unknown')} | "
            f"{lead.get('job_title', 'N/A')} | "
            f"{lead.get('industry', 'N/A')} | "
            f"score={lead.get('score', 0)}"
        )
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="High-level lead generation tool")
    parser.add_argument("--count", type=int, default=5, help="Number of leads to generate")
    parser.add_argument("--output", default="leads.csv", help="CSV path to export generated leads")
    parser.add_argument("--show", action="store_true", help="Print generated leads to the console")
    args = parser.parse_args()

    generator = LeadGenerator()
    leads = generator.generate_batch(args.count)

    if args.show:
        print(_format_leads(leads))

    with open(args.output, "w", newline="", encoding="utf-8") as csv_file:
        generator.export_csv(leads, csv_file)

    print(f"Generated {len(leads)} leads and exported them to {args.output}.")


if __name__ == "__main__":
    main()
