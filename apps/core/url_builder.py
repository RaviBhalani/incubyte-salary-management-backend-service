from yarl import URL


def build_url(
    base: str,
    *parts: str,
    trailing_slash: bool = True,
    **query,
) -> str:
    """
    Builds internal API paths and external 3rd party URLs.
    """
    url = URL(base)
    for p in parts:
        url = url / p

    if trailing_slash and not url.path.endswith("/"):
        url = url.with_path(url.path + "/")

    if query:
        url = url.with_query(query)

    return str(url)