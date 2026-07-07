from typing import TYPE_CHECKING, List, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BASE_URL, CART_URL, ITEM, BasePage

if TYPE_CHECKING:
    from .cart_page import CartPage
    from .login_page import LoginPage


# Selectors
ADD_BUTTON: str = ".btn_inventory"
REMOVE_BUTTON: str = ADD_BUTTON
CART_BUTTON: str = ".shopping_cart_link"
CART_COUNTER_BADGE: str = ".shopping_cart_badge"

# Labels
CART_COUNTER: str = "Cart Counter"

# Buttons names
REMOVE_FROM_CART = "Remove"


class InventoryPage(BasePage):
    """
    Page object model for the inventory page.

    Inherits from BasePage and provides functionality specific to the inventory page,
    such as accessing the inventory container element.

    Attributes:

    Args:
        page (Page): The Playwright Page object to interact with.
        timeout (int, optional): Default timeout for actions, in milliseconds. Defaults to 10000.
    """

    def __init__(self, page: Page, timeout: int = 10000) -> None:
        """
        Initializes the InventoryPage with a Playwright Page instance and an optional timeout.

        Sets up the locator for the inventory container element.

        Args:
            page (Page): The Playwright Page object to interact with.
            timeout (int, optional): Default timeout for actions, in milliseconds. Defaults to 10000.
        """
        super().__init__(page, timeout)
        self._inventory_logo: Locator = self._page.locator(".app_logo")

        self._hamburger_button: Locator = self._page.get_by_role(
            "button", name="Open Menu"
        )
        self._left_menu: Locator = self._page.locator(".bm-menu")
        self._left_menu_item: Locator = self._left_menu.locator(".menu-item")
        self._logout_link: Locator = self._left_menu.get_by_role("link", name="Logout")

        self._products_title: Locator = self._page.locator(".title")
        self._products_filter: Locator = self._page.get_by_role("combobox")

        self._all_items_container: Locator = self._page.locator(".inventory_list")
        self._item: Locator = self._page.locator(".inventory_item")
        self._item_name: Locator = self._page.locator(".inventory_item_name")
        self._item_description: Locator = self._page.locator(".inventory_item_desc")
        self._item_price: Locator = self._page.locator(".inventory_item_price")
        self._add_to_cart_button: Locator = self._page.locator(ADD_BUTTON)
        self._remove_button: Locator = self._page.locator(REMOVE_BUTTON)

        self._cart_button: Locator = self._page.locator(CART_BUTTON)
        self._cart_counter: Locator = self._cart_button.locator(CART_COUNTER_BADGE)

    def get_hamburger_button(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        self._hamburger_button.wait_for(state="visible", timeout=timeout_ms)
        return self._hamburger_button

    def open_hamburger_button(self, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()

    def is_left_menu_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._left_menu.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_left_menu_elements(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_left_menu_displayed(timeout_ms):
            try:
                all_items: List[Locator] = self._left_menu_item.all()
                return [item.inner_text().strip() for item in all_items]
            except PlaywrightTimeoutError:
                raise RuntimeError(
                    f"Timed out waiting for left menu (after {timeout_ms} ms)"
                )
        else:
            raise RuntimeError(f"Left menu was not displayed (after {timeout_ms} ms)")

    def logout(self, timeout: Optional[int] = None) -> "LoginPage":
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()
        self._logout_link.wait_for(state="visible", timeout=timeout_ms)
        self._logout_link.click()
        try:
            self.wait_for_url(BASE_URL, timeout=timeout_ms)
            # local import to avoid circular import
            from .login_page import LoginPage

            return LoginPage(self._page)
        except RuntimeError as exception:
            raise RuntimeError(
                f"Timed out waiting for logout to reach {BASE_URL} after {timeout_ms} ms"
            ) from exception

    def get_document_title(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._inventory_logo.wait_for(state="visible", timeout=timeout_ms)
        return self._page.title().strip()

    def get_logo_text(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._inventory_logo.wait_for(state="visible", timeout=timeout_ms)
        return self._inventory_logo.inner_text().strip()

    def get_products_title(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._products_title.wait_for(state="visible", timeout=timeout_ms)
        return self._products_title.inner_text().strip()

    def is_products_filter_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._products_filter.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_products_filter_object(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_products_filter_displayed(timeout=timeout_ms):
            return self._products_filter
        raise RuntimeError(
            f"Timed out waiting for products filter to be displayed (after {timeout_ms} ms)"
        )

    def get_products_filter_options(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        filter_options: List[Locator] = (
            self.get_products_filter_object(timeout=timeout_ms).locator("option").all()
        )
        all_prices_filter_options: List[str] = [
            filter.inner_text().strip()
            for filter in filter_options
            if filter.inner_text().strip()
        ]
        return all_prices_filter_options

    def get_products_filter_selected_option(self) -> str:
        return self._page.locator(".active_option").inner_text().strip()

    def set_products_filter(self, option: str) -> None:
        self.get_products_filter_object().select_option(option)

    def is_all_items_container_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._all_items_container.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_all_products_names(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_all_items_container_displayed(timeout=timeout_ms):
            all_products_names: List[str] = [
                item.inner_text().strip() for item in self._item_name.all()
            ]
            return all_products_names
        raise RuntimeError(
            f"Timed out waiting for all container items to be displayed (after {timeout_ms} ms)"
        )

    def get_all_products_descriptions(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_all_items_container_displayed(timeout=timeout_ms):
            all_products_descriptions: List[str] = [
                item.inner_text().strip() for item in self._item_description.all()
            ]
            return all_products_descriptions
        raise RuntimeError(
            f"Timed out waiting for all container items to be displayed (after {timeout_ms} ms)"
        )

    def get_all_products_prices(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_all_items_container_displayed(timeout=timeout_ms):
            all_products_price: List[str] = [
                item.inner_text().strip() for item in self._item_price.all()
            ]
            return all_products_price
        raise RuntimeError(
            f"Timed out waiting for all container items to be displayed (after {timeout_ms} ms)"
        )

    def get_all_products_information(
        self, timeout: Optional[int] = None
    ) -> dict[str, dict[str, str]]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_inventory_items_names: List[str] = self.get_all_products_names(timeout_ms)
        all_inventory_items_descriptions: List[str] = (
            self.get_all_products_descriptions(timeout_ms)
        )
        all_inventory_items_prices: List[str] = self.get_all_products_prices(timeout_ms)

        inventory_items_data: dict[str, dict[str, str]] = dict()
        try:
            for name, description, price in zip(
                all_inventory_items_names,
                all_inventory_items_descriptions,
                all_inventory_items_prices,
                strict=True,
            ):
                inventory_items_data[name] = {
                    "description": description,
                    "price": price,
                }
            return inventory_items_data
        except ValueError as exception:
            raise RuntimeError(
                "The arguments (name, description, and price) for zip have different lengths, this means that some inventory items have missing properties."
            ) from exception

    def are_items_images_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms = self._timeout_ms(timeout)

        is_item_image_displayed = list()
        if self.is_all_items_container_displayed(timeout_ms):
            items_names: List[str] = self.get_all_products_names()
            for name in items_names:
                visibility_flag = False
                try:
                    image: Locator = self._page.get_by_role("img", name=name)
                    image.wait_for(state="visible", timeout=timeout_ms)
                except PlaywrightTimeoutError:
                    visibility_flag = False
                else:
                    visibility_flag: bool = True
                finally:
                    is_item_image_displayed.append(visibility_flag)
        return all(is_item_image_displayed)

    def get_cart_page(self, timeout: Optional[int] = None) -> "CartPage":
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._cart_button.wait_for(state="visible", timeout=timeout_ms)
            self._cart_button.click()

            from .cart_page import CartPage

            return CartPage(self._page)
        except PlaywrightTimeoutError:
            raise RuntimeError(
                f"Timed out waiting for inventory to reach {CART_URL} after {timeout_ms} ms"
            )

    def add_item_to_cart(self, index, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        item: Locator = self.get_element(
            self._item.nth(index), f"{ITEM}{index}", timeout_ms
        )
        item.locator(ADD_BUTTON).click(timeout=timeout_ms)

    def remove_item_from_cart(self, index, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        item: Locator = self.get_element(
            self._item.nth(index), f"{ITEM}{index}", timeout_ms
        )
        item.locator(REMOVE_BUTTON).click(timeout=timeout_ms)

    def get_cart_counter(self, timeout: Optional[int] = None) -> int:
        timeout_ms: int = self._timeout_ms(timeout)
        cart_counter: Locator = self.get_element(
            self._cart_counter, CART_COUNTER, timeout_ms
        )
        counter: str = cart_counter.inner_text().strip()
        try:
            return int(counter)
        except ValueError:
            raise RuntimeError(
                f"{CART_COUNTER} is returning a value that cannot be converted to int"
            )

    def is_cart_empty(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._cart_counter.wait_for(state="hidden", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False
