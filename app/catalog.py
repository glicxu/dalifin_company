from __future__ import annotations

from typing import Any


PRODUCT_CATALOG: dict[str, dict[str, Any]] = {
    "mobile_bible": {
        "headline": "Scripture study built for the phone, not squeezed onto it.",
        "summary": "Fast reading, practical study tools, and an install flow that stays simple for church users.",
        "accent": "sunrise",
        "hero_label": "Mobile Bible",
        "features": [
            "Quick reading and study workflows on Android.",
            "Direct APK download from the canonical release feed.",
            "Release notes and version metadata pulled from app_server.",
        ],
        "faq": [
            {
                "question": "How do I install it?",
                "answer": "Download the APK to your Android device, open the file, and allow installation if Android prompts for permission.",
            },
            {
                "question": "Where does version data come from?",
                "answer": "The latest version, file metadata, and artifact link come directly from the app_server download API.",
            },
        ],
    },
    "mobile_trade": {
        "headline": "Dalifin market workflows on Android.",
        "summary": "A tighter delivery page for shipping Android builds without turning the company site into a release registry.",
        "accent": "harbor",
        "hero_label": "Mobile Trade",
        "features": [
            "Operator-published builds surfaced through one API contract.",
            "Consistent product page structure for future app launches.",
            "Latest release resolution stays in app_server, not this repo.",
        ],
        "faq": [
            {
                "question": "Is sign-in required?",
                "answer": "If a product later needs access controls, the site can reflect that policy while app_server remains the source of truth.",
            },
            {
                "question": "Does this site host the APK path logic?",
                "answer": "No. The download button uses the canonical artifact URL supplied by app_server.",
            },
        ],
    },
    "inboxdigest": {
        "headline": "Email summaries, delivered with a simpler public download path.",
        "summary": "Reserved for the eventual company-site migration once the generic product flow is fully proven.",
        "accent": "ember",
        "hero_label": "InboxDigest",
        "features": [
            "Presentation copy can live here without changing release publication rules.",
            "Future-facing structure for FAQ and install guidance.",
            "Same API contract as every other product page.",
        ],
        "faq": [
            {
                "question": "Why is this page here already?",
                "answer": "The catalog keeps a stable website-side presentation layer ready even before the final cutover is complete.",
            }
        ],
    },
}


def get_catalog_entry(product_key: str) -> dict[str, Any]:
    return PRODUCT_CATALOG.get(
        product_key,
        {
            "headline": "Dalifin product downloads.",
            "summary": "Canonical release data is provided by app_server; this site owns the presentation layer.",
            "accent": "harbor",
            "hero_label": product_key.replace("_", " ").title(),
            "features": [],
            "faq": [],
        },
    )
