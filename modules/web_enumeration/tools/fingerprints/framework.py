"""
Framework fingerprint detector.
"""

from __future__ import annotations


def detect_frameworks(
    headers: dict,
    html: str,
) -> set[str]:
    """
    Detect frontend and backend frameworks.
    """

    technologies: set[str] = set()

    html = html.lower()

    powered = headers.get("X-Powered-By", "").lower()

    server = headers.get("Server", "").lower()

    all_headers = " ".join(
        f"{k}:{v}".lower()
        for k, v in headers.items()
    )

    #
    # React
    #

    if "__next" in html:
        technologies.add("React")

    if "react" in html:
        technologies.add("React")

    if "data-reactroot" in html:
        technologies.add("React")

    if "_reactrootcontainer" in html:
        technologies.add("React")

    #
    # Next.js
    #

    if "__next" in html:
        technologies.add("Next.js")

    if "_next/static" in html:
        technologies.add("Next.js")

    if "next-head-count" in html:
        technologies.add("Next.js")

    #
    # Vue.js
    #

    if "__vue__" in html:
        technologies.add("Vue.js")

    if "vue.js" in html:
        technologies.add("Vue.js")

    if "data-v-" in html:
        technologies.add("Vue.js")

    #
    # Nuxt.js
    #

    if "__nuxt" in html:
        technologies.add("Nuxt.js")

    if "_nuxt/" in html:
        technologies.add("Nuxt.js")

    #
    # Angular
    #

    if "ng-version" in html:
        technologies.add("Angular")

    if "angular.js" in html:
        technologies.add("Angular")

    if "angular.min.js" in html:
        technologies.add("Angular")

    #
    # Svelte
    #

    if "_app/immutable" in html:
        technologies.add("Svelte")

    if "svelte" in html:
        technologies.add("Svelte")

    #
    # SvelteKit
    #

    if "__sveltekit" in html:
        technologies.add("SvelteKit")

    #
    # Astro
    #

    if "astro-island" in html:
        technologies.add("Astro")

    #
    # Gatsby
    #

    if "gatsby" in html:
        technologies.add("Gatsby")

    #
    # Remix
    #

    if "remix" in html:
        technologies.add("Remix")

    #
    # Ember.js
    #

    if "ember" in html:
        technologies.add("Ember.js")

    #
    # Backbone.js
    #

    if "backbone" in html:
        technologies.add("Backbone.js")

    #
    # Alpine.js
    #

    if "x-data=" in html:
        technologies.add("Alpine.js")

    #
    # jQuery
    #

    if "jquery" in html:
        technologies.add("jQuery")

    #
    # Laravel
    #

    if "laravel" in powered:
        technologies.add("Laravel")

    if "laravel_session" in html:
        technologies.add("Laravel")

    #
    # Symfony
    #

    if "symfony" in html:
        technologies.add("Symfony")

    #
    # CodeIgniter
    #

    if "codeigniter" in html:
        technologies.add("CodeIgniter")

    #
    # CakePHP
    #

    if "cakephp" in html:
        technologies.add("CakePHP")

    #
    # Yii
    #

    if "yii" in html:
        technologies.add("Yii")

    #
    # Django
    #

    if "csrftoken" in html:
        technologies.add("Django")

    if "django" in powered:
        technologies.add("Django")

    #
    # Flask
    #

    if "flask" in powered:
        technologies.add("Flask")

    if "werkzeug" in server:
        technologies.add("Flask")

    #
    # FastAPI
    #

    if "fastapi" in html:
        technologies.add("FastAPI")

    #
    # Express.js
    #

    if "express" in powered:
        technologies.add("Express.js")

    #
    # Node.js
    #

    if "node.js" in powered:
        technologies.add("Node.js")

    if "nodejs" in powered:
        technologies.add("Node.js")

    #
    # ASP.NET
    #

    if "asp.net" in powered:
        technologies.add("ASP.NET")

    if "x-aspnet-version" in all_headers:
        technologies.add("ASP.NET")

    if "x-aspnetmvc-version" in all_headers:
        technologies.add("ASP.NET MVC")

    #
    # Spring Boot
    #

    if "spring" in powered:
        technologies.add("Spring Boot")

    #
    # Ruby on Rails
    #

    if "rails" in powered:
        technologies.add("Ruby on Rails")

    #
    # Phoenix
    #

    if "phoenix" in html:
        technologies.add("Phoenix")

    return technologies