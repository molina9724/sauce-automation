import re
from typing import cast
from urllib.parse import urljoin

from playwright.sync_api import APIResponse, Locator, expect

from po.pages.base_page import BasePage


def general_image_assert(page: BasePage, image: Locator) -> None:
    expect(image).to_be_visible()
    expect(image).to_have_js_property("complete", True)
    expect(image).not_to_have_js_property("naturalWidth", 0)
    expect(image, "Image has an empty src attribute").to_have_attribute(
        "src", re.compile(r"\S+")
    )
    source: str = cast(str, image.get_attribute("src"))
    image_url: str = urljoin(page.page.url, source)
    response: APIResponse = page.page.request.get(image_url)
    expect(response, f"Image request failed: {image_url}").to_be_ok()
