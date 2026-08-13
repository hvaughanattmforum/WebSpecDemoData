"""One-off batch driver: runs build_main_md.generate() + build_pdf() + build_docx_scroll() for every
component folder passed in, deletes the now-superseded pre-temp/-convention main .md that used to sit
directly in Diagrams/ once the new pipeline succeeds for that component, and prints a JSON report per
component to stdout (one line each) so the caller can review before deciding anything further. Not part
of the skill itself -- a throwaway orchestration script for this one full-repo sweep.
"""
import json
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(__file__))
import build_main_md
from build_pdf import build_pdf
from build_docx_scroll import build_docx_scroll

SPECS_ROOT = r"C:\Users\HugoVaughan\ClaudeCode\WebSpecDemoData\specifications"

COMPONENTS = [
    ("TMFC001", "TMFC001-ProductCatalogManagement", "TMFC001_Product_Catalog_Management"),
    ("TMFC002", "TMFC002-ProductOrderCaptureAndValidation", "TMFC002_Product_Order_Capture_Validation"),
    ("TMFC003", "TMFC003-ProductOrderDeliveryOrchestrationAndManagement",
     "TMFC003_Product_Order_Delivery_Orchestration_and_Management"),
    ("TMFC005", "TMFC005-ProductInventory", "TMFC005_Product_Inventory"),
    ("TMFC006", "TMFC006-ServiceCatalogManagement", "TMFC006_Service_Catalog_Management"),
    ("TMFC007", "TMFC007-ServiceOrderManagement", "TMFC007_Service_Order_Management"),
    ("TMFC008", "TMFC008-ServiceInventory", "TMFC008_Service_Inventory"),
    ("TMFC009", "TMFC009-ServiceQualificationManagement", "TMFC009_Service_Qualification"),
    ("TMFC010", "TMFC010-ResourceCatalogManagement", "TMFC010_Resource_Catalog_Management"),
    ("TMFC011", "TMFC011-ResourceOrderManagement", "TMFC011_Resource_Order_Management"),
    ("TMFC012", "TMFC012-ResourceInventory", "TMFC012_Resource_Inventory"),
    ("TMFC014", "TMFC014-LocationManagement", "TMFC014_Location_Management"),
    ("TMFC020", "TMFC020-DigitalIdentityManagement", "TMFC020_Digital_Identity_Management"),
    ("TMFC022", "TMFC022-PartyPrivacyManagement", "TMFC022_Party_Privacy_Management"),
    ("TMFC023", "TMFC023-PartyInteractionManagement", "TMFC023_Party_Interaction_Management"),
    ("TMFC024", "TMFC024-BillingAccountManagement", "TMFC024_Billing_Account_Management"),
    ("TMFC027", "TMFC027-ProductConfigurator", "TMFC027_Product_Configurator"),
    ("TMFC028", "TMFC028-PartyManagement", "TMFC028_Party_Management"),
    ("TMFC029", "TMFC029-PaymentManagement", "TMFC029_Payment_Management"),
    ("TMFC030", "TMFC030-BillGeneration", "TMFC030_Bill_Generation_Management"),
    ("TMFC031", "TMFC031-BillCalculation", "TMFC031_Bill_Calculation_Management"),
    ("TMFC035", "TMFC035-PermissionsManagement", "TMFC035_Permissions_Management"),
    ("TMFC036", "TMFC036-LeadAndOpportunityManagement", "TMFC036_Lead_and_Opportunity_Management"),
    ("TMFC037", "TMFC037-ServicePerformanceManagement", "TMFC037_Service_Performance_Management"),
    ("TMFC038", "TMFC038-ResourcePerformanceManagement", "TMFC038_Resource_Performance_Management"),
    ("TMFC039", "TMFC039-AgreementManagement", "TMFC039_Agreement_Management"),
    ("TMFC040", "TMFC040-ProductUsageManagement", "TMFC040_Product_Usage_Management"),
    ("TMFC041", "TMFC041-AnomalyManagement", "TMFC041_Anomaly_Management"),
    ("TMFC043", "TMFC043-FaultManagement", "TMFC043_Fault_Management"),
    ("TMFC046", "TMFC046-WorkforceManagement", "TMFC046_Workforce_Management"),
    ("TMFC050", "TMFC050-ProductRecommendation", "TMFC050_Product_Recommendation_Management"),
    ("TMFC054", "TMFC054-ProductTestManagement", "TMFC054_Product_Test_Management"),
    ("TMFC055", "TMFC055-ServiceTestManagement", "TMFC055_Service_Test_Management"),
    ("TMFC061", "TMFC061-WorkOrderManagement", "TMFC061_Work_Order_Management"),
    ("TMFC062", "TMFC062-ResourceConfigurationandActivation", "TMFC062_Resource_Configuration_and_Activation"),
]


def run_one(cid, folder, stem):
    component_dir = os.path.join(SPECS_ROOT, folder)
    result = {"id": cid, "folder": folder, "ok": False}
    try:
        gen_report = build_main_md.generate(component_dir, cid, stem)
        result["gen"] = gen_report
        md_path = gen_report["md_path"]
        build_pdf(md_path)
        build_docx_scroll(md_path)
        stale_md = os.path.join(component_dir, "Diagrams", f"{stem}.md")
        if os.path.exists(stale_md):
            os.remove(stale_md)
            result["removed_stale_md"] = True
        result["ok"] = True
    except Exception:
        result["error"] = traceback.format_exc()
    return result


if __name__ == "__main__":
    only = sys.argv[1:] or None
    results = []
    for cid, folder, stem in COMPONENTS:
        if only and cid not in only:
            continue
        r = run_one(cid, folder, stem)
        results.append(r)
        print(json.dumps(r, default=str))
        sys.stdout.flush()
