from sauce_project.po.components.left_menu import LeftMenu
from sauce_project.po.pages.base_page import LOGIN_URL
from sauce_project.po.pages.login_page import LoginPage


def logout(left_menu: LeftMenu) -> None:
    login_page: LoginPage = left_menu.logout()
    assert login_page.get_url() == LOGIN_URL
