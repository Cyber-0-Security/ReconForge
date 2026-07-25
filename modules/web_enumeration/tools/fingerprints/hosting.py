"""
Hosting and cloud provider fingerprint detector.
"""

from __future__ import annotations


def detect_hosting(
    headers: dict,
    html: str,
) -> set[str]:
    """
    Detect hosting providers and cloud platforms.
    """

    technologies: set[str] = set()

    html = html.lower()

    server = headers.get("Server", "").lower()

    powered = headers.get("X-Powered-By", "").lower()

    all_headers = {
        k.lower(): str(v).lower()
        for k, v in headers.items()
    }

    headers_text = " ".join(
        f"{k}:{v}"
        for k, v in all_headers.items()
    )

    #
    # Amazon Web Services
    #

    if "amazon" in server:
        technologies.add("Amazon Web Services")

    if "awselb" in server:
        technologies.add("Amazon Web Services")

    if "x-amz" in headers_text:
        technologies.add("Amazon Web Services")

    if "amazonaws.com" in html:
        technologies.add("Amazon Web Services")

    #
    # Microsoft Azure
    #

    if "azure" in headers_text:
        technologies.add("Microsoft Azure")

    if "azurewebsites.net" in html:
        technologies.add("Microsoft Azure")

    if "azureedge.net" in html:
        technologies.add("Microsoft Azure")

    #
    # Google Cloud Platform
    #

    if "googleusercontent.com" in html:
        technologies.add("Google Cloud Platform")

    if "gstatic.com" in html:
        technologies.add("Google Cloud Platform")

    if "appspot.com" in html:
        technologies.add("Google App Engine")

    #
    # Firebase
    #

    if "firebase" in html:
        technologies.add("Firebase")

    if "firebaseapp.com" in html:
        technologies.add("Firebase Hosting")

    #
    # Cloudflare Pages
    #

    if "pages.dev" in html:
        technologies.add("Cloudflare Pages")

    #
    # Netlify
    #

    if "netlify" in server:
        technologies.add("Netlify")

    if "netlify.app" in html:
        technologies.add("Netlify")

    #
    # Vercel
    #

    if "vercel" in powered:
        technologies.add("Vercel")

    if "x-vercel-id" in all_headers:
        technologies.add("Vercel")

    if "vercel.app" in html:
        technologies.add("Vercel")

    #
    # Render
    #

    if "render.com" in html:
        technologies.add("Render")

    if "onrender.com" in html:
        technologies.add("Render")

    #
    # Railway
    #

    if "railway.app" in html:
        technologies.add("Railway")

    #
    # Fly.io
    #

    if "fly.dev" in html:
        technologies.add("Fly.io")

    if "fly.io" in html:
        technologies.add("Fly.io")

    #
    # Heroku
    #

    if "herokuapp.com" in html:
        technologies.add("Heroku")

    if "heroku" in server:
        technologies.add("Heroku")

    #
    # DigitalOcean
    #

    if "digitaloceanspaces.com" in html:
        technologies.add("DigitalOcean")

    #
    # Linode
    #

    if "linode" in html:
        technologies.add("Linode")

    #
    # Vultr
    #

    if "vultr" in html:
        technologies.add("Vultr")

    #
    # OVH
    #

    if "ovh" in html:
        technologies.add("OVHcloud")

    #
    # Hetzner
    #

    if "hetzner" in html:
        technologies.add("Hetzner")

    #
    # GitHub Pages
    #

    if "github.io" in html:
        technologies.add("GitHub Pages")

    #
    # GitLab Pages
    #

    if "gitlab.io" in html:
        technologies.add("GitLab Pages")

    #
    # Oracle Cloud
    #

    if "oraclecloud.com" in html:
        technologies.add("Oracle Cloud")

    #
    # Alibaba Cloud
    #

    if "aliyuncs.com" in html:
        technologies.add("Alibaba Cloud")

    #
    # IBM Cloud
    #

    if "mybluemix.net" in html:
        technologies.add("IBM Cloud")

    return technologies