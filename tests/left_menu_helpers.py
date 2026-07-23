from sauce_project.po.components.left_menu import LeftMenu
from sauce_project.po.pages.base_page import INVENTORY_URL, LOGIN_URL
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage


def logout(left_menu: LeftMenu) -> LoginPage:
    login_page: LoginPage = left_menu.logout()
    assert login_page.get_url() == LOGIN_URL
    return login_page


def all_items(left_menu: LeftMenu) -> InventoryPage:
    inventory_page: InventoryPage = left_menu.all_items()
    assert inventory_page.get_url() == INVENTORY_URL
    return inventory_page
