"""
Chat and customer support fingerprint detector.
"""

from __future__ import annotations


def detect_chat(html: str) -> set[str]:
    """
    Detect live chat and customer support platforms.
    """

    technologies: set[str] = set()

    html = html.lower()

    #
    # Intercom
    #

    if "intercom" in html:
        technologies.add("Intercom")

    if "widget.intercom.io" in html:
        technologies.add("Intercom")

    #
    # Zendesk
    #

    if "zendesk" in html:
        technologies.add("Zendesk")

    if "zdassets.com" in html:
        technologies.add("Zendesk")

    #
    # Tawk.to
    #

    if "tawk.to" in html:
        technologies.add("Tawk.to")

    if "embed.tawk.to" in html:
        technologies.add("Tawk.to")

    #
    # Crisp
    #

    if "crisp.chat" in html:
        technologies.add("Crisp")

    if "client.crisp.chat" in html:
        technologies.add("Crisp")

    #
    # Drift
    #

    if "drift.com" in html:
        technologies.add("Drift")

    if "js.driftt.com" in html:
        technologies.add("Drift")

    #
    # LiveChat
    #

    if "livechatinc.com" in html:
        technologies.add("LiveChat")

    if "cdn.livechatinc.com" in html:
        technologies.add("LiveChat")

    #
    # Freshchat
    #

    if "freshchat" in html:
        technologies.add("Freshchat")

    if "fw-cdn.com" in html:
        technologies.add("Freshchat")

    #
    # HubSpot Chat
    #

    if "hubspot" in html:
        technologies.add("HubSpot Chat")

    if "js.hs-scripts.com" in html:
        technologies.add("HubSpot Chat")

    #
    # Olark
    #

    if "olark.com" in html:
        technologies.add("Olark")

    #
    # Zoho SalesIQ
    #

    if "salesiq" in html:
        technologies.add("Zoho SalesIQ")

    if "zoho" in html:
        technologies.add("Zoho SalesIQ")

    #
    # Tidio
    #

    if "tidio" in html:
        technologies.add("Tidio")

    if "code.tidio.co" in html:
        technologies.add("Tidio")

    #
    # Smartsupp
    #

    if "smartsupp" in html:
        technologies.add("Smartsupp")

    #
    # Help Scout
    #

    if "helpscout" in html:
        technologies.add("Help Scout")

    #
    # Userlike
    #

    if "userlike" in html:
        technologies.add("Userlike")

    #
    # JivoChat
    #

    if "jivosite" in html:
        technologies.add("JivoChat")

    #
    # Chaport
    #

    if "chaport" in html:
        technologies.add("Chaport")

    #
    # Comm100
    #

    if "comm100" in html:
        technologies.add("Comm100")

    #
    # LivePerson
    #

    if "liveperson" in html:
        technologies.add("LivePerson")

    #
    # Gorgias
    #

    if "gorgias.chat" in html:
        technologies.add("Gorgias")

    return technologies