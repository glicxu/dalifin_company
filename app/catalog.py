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
    "interprete": {
        "headline": "Join Dali Interpreter sessions from your phone.",
        "summary": "A listener-focused Android build for live interpretation sessions, with app audio that is more reliable than a browser tab.",
        "accent": "harbor",
        "hero_label": "Dali Interpreter Listener",
        "features": [
            "Listen to live translated audio with fewer browser playback interruptions.",
            "Join public sessions quickly and sign in when a private session requires it.",
            "Use replay and rejoin controls designed for longer interpretation sessions.",
        ],
        "faq": [
            {
                "question": "Do I need AI settings in the listener app?",
                "answer": "No. Listener builds only need the server address and account sign-in when a session requires private access.",
            },
            {
                "question": "Should iPhone users use this APK?",
                "answer": "No. iPhone users should use the Dali Interpreter Listener TestFlight beta link from the web listener page.",
            },
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
