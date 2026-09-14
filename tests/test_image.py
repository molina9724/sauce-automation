from urllib.parse import urljoin

from playwright.sync_api import APIResponse, Locator, expect

from po.pages.base_page import BasePage


def general_image_assert(page: BasePage, image: Locator) -> None:
    expect(image).to_be_visible()
    expect(image).to_have_js_property("complete", True)
    expect(image).not_to_have_js_property("naturalWidth", 0)
    source: str | None = image.get_attribute("src")
    # TODO: Investigate replacing this Python assert with a Playwright attribute assertion
    assert source
    image_url: str = urljoin(page.page.url, source)
    response: APIResponse = page.page.request.get(image_url)
    expect(response).to_be_ok()
