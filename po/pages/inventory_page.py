from typing import TYPE_CHECKING, List, Optional

from playwright.sync_api import Locator, Page

# fmt: off
from .base_page import (BASE_URL, CART_BUTTON, CART_COUNTER_BADGE, CART_URL,
                        ITEM, ITEM_DESCRIPTION, ITEM_NAME, ITEM_PRICE,
                        BasePage)

# fmt: on

if TYPE_CHECKING:
    from .cart_page import CartPage
    from .login_page import LoginPage


# Selectors
ADD_BUTTON: str = ".btn_inventory"
REMOVE_BUTTON: str = ADD_BUTTON
LEFT_MENU_ITEM: str = ".menu-item"

# Labels
CART_COUNTER: str = "Cart Counter"
ITEMS_CONTAINER: str = "Items Container"
SORT_FILTER: str = "Sort Filter"
PRODUCTS_TITLE: str = "Products Title"
LOGO_TEXT: str = "Logo Text"
DOCUMENT_TITLE: str = "Document Title"
HAMBURGER_BUTTON: str = "Hamburger Button"
LOGOUT_LINK: str = "Logout Link"
LEFT_MENU: str = "Left Menu"

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
        self._left_menu_item: Locator = self._left_menu.locator(LEFT_MENU_ITEM)
        self._logout_link: Locator = self._left_menu.get_by_role("link", name="Logout")

        self._products_title: Locator = self._page.locator(".title")
        self._products_filter: Locator = self._page.get_by_role("combobox")

        self._all_items_container: Locator = self._page.locator(".inventory_list")
        self._item: Locator = self._page.locator(".inventory_item")
        self._item_name: Locator = self._item.locator(ITEM_NAME)
        self._item_description: Locator = self._item.locator(ITEM_DESCRIPTION)
        self._item_price: Locator = self._item.locator(ITEM_PRICE)
        self._item_image: Locator = self._item.locator(
            "img[class='inventory_item_img']"
        )
        self._add_to_cart_button: Locator = self._item.locator(ADD_BUTTON)
        self._remove_button: Locator = self._item.locator(REMOVE_BUTTON)

    def get_hamburger_button(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        hamburger_button: Locator = self.get_element(
            self._hamburger_button, HAMBURGER_BUTTON, timeout_ms
        )
        return hamburger_button

    def open_hamburger_button(self, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()

    def get_logout_link(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        logout: Locator = self.get_element(self._logout_link, LOGOUT_LINK, timeout_ms)
        return logout

    def is_left_menu_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._left_menu, timeout_ms)

    def get_left_menu_elements(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        left_menu: Locator = self.get_element(self._left_menu, LEFT_MENU, timeout_ms)
        all_items: List[Locator] = left_menu.locator(LEFT_MENU_ITEM).all()
        return [item.inner_text().strip() for item in all_items]

    def logout(self, timeout: Optional[int] = None) -> "LoginPage":
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()
        self.get_logout_link(timeout_ms).click()
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
        self.get_element(self._inventory_logo, DOCUMENT_TITLE, timeout_ms)
        return self._page.title().strip()

    def get_logo_text(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        logo: Locator = self.get_element(self._inventory_logo, LOGO_TEXT, timeout_ms)
        return logo.inner_text().strip()

    def get_products_title(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        products_title: Locator = self.get_element(
            self._products_title, PRODUCTS_TITLE, timeout_ms
        )
        return products_title.inner_text().strip()

    def is_products_filter_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._products_filter, timeout_ms)

    def get_products_filter_options(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        sort_filter: Locator = self.get_element(
            self._products_filter, SORT_FILTER, timeout_ms
        )
        filter_options: List[Locator] = sort_filter.locator("option").all()
        all_prices_filter_options: List[str] = [
            filter_option.inner_text().strip()
            for filter_option in filter_options
            if filter_option.inner_text().strip()
        ]
        return all_prices_filter_options

    def get_products_filter_selected_option(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        selected_filter: Locator = self.get_element(
            self._page.locator(".active_option"), SORT_FILTER, timeout_ms
        )
        return selected_filter.inner_text().strip()

    def set_products_filter(self, option: str, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        filter_options: Locator = self.get_element(
            self._products_filter, SORT_FILTER, timeout_ms
        )
        filter_options.select_option(option)

    def is_all_items_container_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._all_items_container, timeout_ms)

    # get_all_products_names, get_all_products_descriptions, get_all_products_prices aren't refactored since data might change in the future
    def get_all_products_names(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        names: List[str] = []
        for index, item in enumerate(self._item.all()):
            name: Locator = self.get_element(
                item.locator(ITEM_NAME),
                f"{ITEM_NAME} for {ITEM}{index}",
                timeout_ms,
            )
            names.append(name.inner_text().strip())
        return names

    def get_all_products_descriptions(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        descriptions: List[str] = []
        for index, item in enumerate(self._item.all()):
            description: Locator = self.get_element(
                item.locator(ITEM_DESCRIPTION),
                f"{ITEM_DESCRIPTION} for {ITEM}{index}",
                timeout_ms,
            )
            descriptions.append(description.inner_text().strip())
        return descriptions

    def get_all_products_prices(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        prices: List[str] = []
        for index, item in enumerate(self._item.all()):
            price: Locator = self.get_element(
                item.locator(ITEM_PRICE), f"{ITEM_PRICE} for {ITEM}{index}", timeout_ms
            )
            prices.append(price.inner_text().strip())
        return prices

    # TODO: This method should include images and add/remove buttons to consistently test the whole item object
    # TODO: Investigate how to to test images properly
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
        timeout_ms: int = self._timeout_ms(timeout)

        items_names: List[str] = self.get_all_products_names()
        is_item_image_displayed: List[bool] = list()
        for index in range(len(items_names)):
            visibility_flag: bool = False
            try:
                self.get_element(
                    self._item_image.nth(index), f"{ITEM}{index}", timeout_ms
                )
                visibility_flag = True
            except RuntimeError:
                visibility_flag = False
            finally:
                is_item_image_displayed.append(visibility_flag)
        return all(is_item_image_displayed)

    def get_cart_page(self, timeout: Optional[int] = None) -> "CartPage":
        timeout_ms: int = self._timeout_ms(timeout)
        cart_button: Locator = self.get_element(self._cart_button, CART_URL, timeout_ms)
        cart_button.click()
        from .cart_page import CartPage

        return CartPage(self._page)

    def add_item_to_cart(self, index: int, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        item: Locator = self.get_element(
            self._item.nth(index), f"{ITEM}{index}", timeout_ms
        )
        item.locator(ADD_BUTTON).click(timeout=timeout_ms)

    def remove_item_from_cart(self, index: int, timeout: Optional[int] = None) -> None:
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
