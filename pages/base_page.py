class BasePage:
    def __init__(self, browser):
        self.browser = browser
    
    def find(self, args):
        return self.browser.find_element(*args)
    
    def find_element_from_block(self, element, args):
        return element.find_element(*args)
    
    def find_elements_from_block(self, elements, args):
        return elements.find_elements(*args)