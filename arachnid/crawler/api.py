from .crawler import Crawler, CrawlerConfig


def get_crawler(namespace):
    return Crawler(namespace.seed, config=_generate_crawler_config(namespace))


def _generate_crawler_config(namespace):
    """ Given a namespace provided by argparse, convert to a config the crawler can interpret """
    config = CrawlerConfig()
    # Apply pre-configs
    if "stealth" in namespace:
        config.set_stealth()
    elif "aggressive" in namespace:
        config.set_aggressive()

    # Parse --find options given by user
    if "find" in namespace:
        supplied_options = [opt.lower() for opt in namespace.find]
        if "all" in supplied_options and "none" in supplied_options:
            print("\"all\" and \"none\" options are mutually exclusive in --find")
            raise SystemExit
        has_occurred = {
                    "phone": False,
                    "email": False,
                    "social": False,
                    "docs": False,
                     }
        if "all" in supplied_options:
            for k in has_occurred:
                has_occurred[k] = True
        elif "none" in supplied_options:
            for k in has_occurred:
                has_occurred[k] = False
        else:
            for k in has_occurred:
                if k in supplied_options:
                    has_occurred[k] = True
        config.scrape_phone_number = has_occurred["phone"]
        config.scrape_email = has_occurred["email"]
        config.scrape_social_media = has_occurred["social"]
        if not has_occurred["docs"]:
            config.documents = set()

    config.documents.update(namespace.custom_doc)

    # Apply all argparse arguments that are can be directly translated
    for k, v in vars(namespace).items():
        if hasattr(config, k):
            setattr(config, k, v)

    return config
