from pages.base_page import BasePage


class CompanyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.header = Header(driver, self)

    PATH = '/ui/companies'
    VIEW_BUTTON = './/svg[@class="icon eye-icon"]'
    UPDATE_INFO_BUTTON = './/svg[@class="icon pencil-icon  "]'
    DELETE_BUTTON = './/svg[@class="icon trash-icon  "]'

    def get_company_item(self, cmp_id: int = 2):
        return f'//div[data-company-id="{str(cmp_id)}"]'

    def click_button_companies(self, button: Literal['view','update','delete'], cmp_id: int = 2) -> None:
        button_name = {'view': self.VIEW_BUTTON,
                       'update': self.UPDATE_INFO_BUTTON,
                       'delete': self.DELETE_BUTTON}
        if button not in button_name:
            raise ValueError(f'Неизвестная кнопка: {button}')
        selected_button = button_name[button]
        company = self.find_element(self.get_company_item(cmp_id))
        btn = company.find_element(By.XPATH, selected_button)
        self.click_element(btn)

