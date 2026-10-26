import csv
import io

from leadgen import LeadGenerator


def test_score_lead_prefers_high_intent_and_fit():
    generator = LeadGenerator()
    lead = {
        "company": "Northwind Analytics",
        "industry": "SaaS",
        "job_title": "VP of Revenue",
        "email": "vp@northwindanalytics.com",
        "budget": 50000,
        "source": "Outbound",
        "pain_points": ["pipeline growth", "lead conversion"],
    }

    score = generator.score_lead(lead)

    assert 0 <= score <= 100
    assert score >= 70


def test_export_leads_writes_csv_rows():
    generator = LeadGenerator()
    leads = [
        {
            "company": "Acme Labs",
            "industry": "Healthcare",
            "job_title": "Operations Director",
            "email": "ops@acme.com",
            "budget": 40000,
            "source": "Referral",
            "pain_points": ["manual follow-up"],
        }
    ]

    output = io.StringIO()
    generator.export_csv(leads, output)

    rows = list(csv.DictReader(io.StringIO(output.getvalue())))
    assert len(rows) == 1
    assert rows[0]["company"] == "Acme Labs"
    assert rows[0]["industry"] == "Healthcare"


def test_generate_batch_creates_quality_leads():
    generator = LeadGenerator()
    leads = generator.generate_batch(3)

    assert len(leads) == 3
    assert all("company" in lead for lead in leads)
    assert all("score" in lead for lead in leads)
