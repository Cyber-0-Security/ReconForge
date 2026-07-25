"""
CMS fingerprint detector.
"""

from __future__ import annotations


def detect_cms(
    headers: dict,
    html: str,
    cookies,
) -> set[str]:
    """
    Detect Content Management Systems.
    """

    technologies: set[str] = set()

    html = html.lower()

    all_headers = " ".join(
        f"{k}:{v}".lower()
        for k, v in headers.items()
    )

    cookie_names = {
        cookie.name.lower()
        for cookie in cookies
    }

    #
    # WordPress
    #

    if "/wp-content/" in html:
        technologies.add("WordPress")

    if "/wp-includes/" in html:
        technologies.add("WordPress")

    if "wp-json" in html:
        technologies.add("WordPress")

    if "wordpress" in html:
        technologies.add("WordPress")

    if any(name.startswith("wordpress") for name in cookie_names):
        technologies.add("WordPress")

    #
    # Joomla
    #

    if "/media/system/js/" in html:
        technologies.add("Joomla")

    if "/templates/" in html:
        technologies.add("Joomla")

    if "joomla" in html:
        technologies.add("Joomla")

    #
    # Drupal
    #

    if "/sites/default/" in html:
        technologies.add("Drupal")

    if "drupal-settings-json" in html:
        technologies.add("Drupal")

    if "drupal" in html:
        technologies.add("Drupal")

    #
    # Magento
    #

    if "/static/frontend/" in html:
        technologies.add("Magento")

    if "mage/" in html:
        technologies.add("Magento")

    if "magento" in html:
        technologies.add("Magento")

    #
    # Shopify
    #

    if "cdn.shopify.com" in html:
        technologies.add("Shopify")

    if "shopify.theme" in html:
        technologies.add("Shopify")

    if "_shopify" in html:
        technologies.add("Shopify")

    #
    # Wix
    #

    if "wixstatic.com" in html:
        technologies.add("Wix")

    if "_wixcss" in html:
        technologies.add("Wix")

    if "wix" in html:
        technologies.add("Wix")

    #
    # Squarespace
    #

    if "static.squarespace.com" in html:
        technologies.add("Squarespace")

    if "squarespace" in html:
        technologies.add("Squarespace")

    #
    # Ghost
    #

    if "/ghost/" in html:
        technologies.add("Ghost CMS")

    if "ghost-content" in html:
        technologies.add("Ghost CMS")

    #
    # Blogger
    #

    if "blogger.com" in html:
        technologies.add("Blogger")

    if "blogspot.com" in html:
        technologies.add("Blogger")

    #
    # TYPO3
    #

    if "typo3" in html:
        technologies.add("TYPO3")

    #
    # Umbraco
    #

    if "umbraco" in html:
        technologies.add("Umbraco")

    #
    # Craft CMS
    #

    if "craftcms" in html:
        technologies.add("Craft CMS")

    #
    # October CMS
    #

    if "octobercms" in html:
        technologies.add("October CMS")

    #
    # ExpressionEngine
    #

    if "exp:" in html:
        technologies.add("ExpressionEngine")

    #
    # OpenCart
    #

    if "route=product" in html:
        technologies.add("OpenCart")

    #
    # PrestaShop
    #

    if "prestashop" in html:
        technologies.add("PrestaShop")

    #
    # MediaWiki
    #

    if "mediawiki" in html:
        technologies.add("MediaWiki")

    #
    # DNN
    #

    if "dnn" in all_headers:
        technologies.add("DotNetNuke")

    return technologies