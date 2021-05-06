from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from datetime import datetime

url = 'https://www.saucedemo.com/'

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def test_login(driver, user, password):
    print("#########Test login#########")
    driver.get(url)
    driver.find_element_by_id('user-name').send_keys(user)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_id('login-button').click()
    assert (url+'inventory.html') in driver.current_url, "Login failed"
    print(f"Login succeeded at {timestamp()}")

def test_add_to_cart(driver, n_products):
    print(f"#########Test adding {n_products} products to cart#########")
    assert (n_products > 0 & n_products < 7), "There are six products in the inventory"
    products_added = []
    for i in range(n_products):
        product_url = url + f"inventory-item.html?id={i}"
        driver.get(product_url)
        driver.find_element_by_class_name('btn_inventory').click()
        products_added.append(
            driver.find_element_by_class_name('inventory_details_name').text)
    print(f"Added {', '.join(products_added)} to cart")
    driver.get(url + "cart.html")
    products_in_cart = [x.text for x in 
                        driver.find_elements_by_class_name('inventory_item_name')]
    print("The cart has: ", ', '.join(products_in_cart))
    assert set(products_added) <= set(products_in_cart)
    print(f"Adding products succeeded at {timestamp()}")

def test_remove(driver, n_products):
    print(f"#########Test removing products from the cart#########")
    driver.get(url + "cart.html")
    products_in_cart = [x.text for x in 
                        driver.find_elements_by_class_name('inventory_item_name')]
    print(f"Removing {n_products} products from cart")
    n_products_in_cart = len(products_in_cart)
    assert (n_products <= n_products_in_cart), f"There are {n_products_in_cart} products in cart"
    buttons = driver.find_elements_by_class_name('cart_button')
    products_removed = []
    for i in range(n_products):
        buttons[i].click()
        products_removed.append(products_in_cart[i])
    print(f"Removed: ", ', '.join(products_removed))
    assert set(products_removed) <= set(products_in_cart)
    print(f"Removing products succeeded at {timestamp()}")

if __name__ == "__main__":
    print ('Starting the browser...')
    options = ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    test_login(driver, 'standard_user', 'secret_sauce')
    test_add_to_cart(driver, 3) 
    test_remove(driver, 2)