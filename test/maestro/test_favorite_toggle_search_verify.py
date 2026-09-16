"""
Bringapp Cafe - Favorite Toggle and Search Verification

Scenario:
- User logs in with demo credentials
- User marks Classic Cheeseburger as favorite on Home screen
- User navigates to Favorites tab and confirms the burger appears
- User navigates to Search tab and searches for "Pizza"
- User verifies pizza items are listed in search results
- User returns to Home screen
- User un-favorites the Classic Cheeseburger
- User navigates to Favorites tab and confirms "No favorites yet!" message appears

Platform: android
Brand: bringapp_cafe
Environment: qa
TestCaseID: favoriteClassicCheeseburger
"""

import pytest
import time
from input.data import load_test_data

from apps.bringapp_cafe.helpers.screens.auth_screen import AuthScreen
from apps.bringapp_cafe.helpers.screens.home_screen import HomeScreen
from apps.bringapp_cafe.helpers.screens.favorites_screen import FavoritesScreen
from helper_add.bringapp_cafe.home_screen import HomeScreen as ExtendedHomeScreen
from helper_add.bringapp_cafe.favorites_screen import FavoritesScreen as ExtendedFavoritesScreen


def test_favorite_toggle_search_verify(driver):
    """
    Test: User favorites a burger, searches for items, and un-favorites the burger.
    
    Steps:
    1. Load test data for testcase_id 'favoriteClassicCheeseburger'
    2. Initialize screen helpers
    3. Log in with demo credentials
    4. Verify home screen is displayed
    5. Mark Classic Cheeseburger as favorite
    6. Navigate to Favorites tab and verify the burger appears
    7. Navigate to Search tab and search for "Pizza"
    8. Verify pizza items appear in search results
    9. Return to Home screen
    10. Un-favorite the Classic Cheeseburger
    11. Navigate to Favorites tab and verify "No favorites yet!" message
    """
    # Load test data
    testcase_id = "favoriteClassicCheeseburger"
    data = load_test_data(testcase_id, app_id="bringapp_cafe")
    
    username = data.get("Username")
    password = data.get("Password")
    product = data.get("Product")
    
    print(f"\n[TEST] Starting favorite toggle and search verification test")
    print(f"[TEST] Username: {username}")
    print(f"[TEST] Product: {product}")
    
    # Initialize screen helpers
    auth_screen = AuthScreen(driver)
    home_screen = HomeScreen(driver)
    extended_home_screen = ExtendedHomeScreen(driver)
    favorites_screen = FavoritesScreen(driver)
    extended_favorites_screen = ExtendedFavoritesScreen(driver)
    
    # ========== STEP 1: LOGIN WITH CREDENTIALS ==========
    print("\n[STEP 1] Logging in with credentials...")
    auth_screen.login_user(username, password)
    print("[STEP 1] ✓ Login successful")
    
    # ========== STEP 2: VERIFY HOME SCREEN IS DISPLAYED ==========
    print("\n[STEP 2] Verifying home screen is displayed...")
    assert home_screen.verify_home_page_loaded(), "Home screen did not load after login"
    print("[STEP 2] ✓ Home screen loaded")
    
    # ========== STEP 3: MARK CLASSIC CHEESEBURGER AS FAVORITE ==========
    print(f"\n[STEP 3] Marking {product} as favorite...")
    home_screen.favorite_classic_cheeseburger()
    time.sleep(1)  # Wait for favorite action to complete
    print(f"[STEP 3] ✓ {product} marked as favorite")
    
    # ========== STEP 4: NAVIGATE TO FAVORITES TAB ==========
    print("\n[STEP 4] Navigating to Favorites tab...")
    home_screen.navigate_to_favorites_tab()
    time.sleep(1)  # Wait for tab transition
    print("[STEP 4] ✓ Navigated to Favorites tab")
    
    # ========== STEP 5: VERIFY BURGER APPEARS IN FAVORITES ==========
    print(f"\n[STEP 5] Verifying {product} appears in Favorites...")
    assert favorites_screen.verify_favorites_screen_displayed(), "Favorites screen did not display"
    
    # Verify the item is in favorites
    try:
        extended_favorites_screen.verify_item_in_favorites(product)
        print(f"[STEP 5] ✓ {product} found in Favorites")
    except AssertionError as e:
        print(f"[STEP 5] ✗ {product} not found in Favorites: {e}")
        raise
    
    # ========== STEP 6: NAVIGATE TO SEARCH TAB ==========
    print("\n[STEP 6] Navigating to Search tab...")
    home_screen.navigate_to_home()  # Go back to home first
    time.sleep(1)
    home_screen.search_for_item("Pizza")
    time.sleep(2)  # Wait for search results to load
    print("[STEP 6] ✓ Navigated to Search tab and searched for 'Pizza'")
    
    # ========== STEP 7: VERIFY PIZZA ITEMS IN SEARCH RESULTS ==========
    print("\n[STEP 7] Verifying pizza items appear in search results...")
    try:
        # On the Search screen, verify that at least one pizza-related item is visible
        # Use XPath to find ImageView elements with content-desc containing "Pizza"
        from appium.webdriver.common.appiumby import AppiumBy
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        
        wait = WebDriverWait(driver, 10)
        
        # Look for ImageView elements with content-desc containing "Pizza"
        # This matches items like "BBQ Chicken Pizza", "Pepperoni Pizza", etc.
        xpath = "//android.widget.ImageView[@content-desc and contains(@content-desc, 'Pizza')]"
        
        try:
            search_results = wait.until(
                EC.presence_of_all_elements_located((AppiumBy.XPATH, xpath))
            )
            
            assert len(search_results) > 0, "No pizza items found in search results"
            print(f"[STEP 7] ✓ Found {len(search_results)} pizza item(s) in search results")
            
            # Log the found pizza items for debugging
            for idx, result in enumerate(search_results):
                try:
                    content_desc = result.get_attribute("content-desc")
                    if content_desc:
                        # Extract just the product name (first line before newline)
                        product_name = content_desc.split("\n")[0] if "\n" in content_desc else content_desc
                        print(f"[STEP 7]   Pizza item {idx + 1}: {product_name}")
                except Exception as e:
                    print(f"[STEP 7]   Pizza item {idx + 1}: (could not extract name: {e})")
            
        except Exception as e:
            print(f"[STEP 7] ✗ Failed to find pizza items in search results: {e}")
            raise AssertionError(f"No pizza items found in search results: {e}")
        
    except Exception as e:
        print(f"[STEP 7] ✗ Failed to verify search results: {e}")
        raise AssertionError(f"Failed to verify search results: {e}")
    
    # ========== STEP 8: RETURN TO HOME SCREEN ==========
    print("\n[STEP 8] Returning to Home screen...")
    home_screen.navigate_to_home()
    time.sleep(1)
    assert home_screen.verify_home_page_loaded(), "Home screen did not load"
    print("[STEP 8] ✓ Returned to Home screen")
    
    # ========== STEP 9: UN-FAVORITE THE CLASSIC CHEESEBURGER ==========
    print(f"\n[STEP 9] Un-favoriting {product}...")
    # Tap the favorite button again to un-favorite
    home_screen.favorite_classic_cheeseburger()
    time.sleep(1)  # Wait for un-favorite action to complete
    print(f"[STEP 9] ✓ {product} un-favorited")
    
    # ========== STEP 10: NAVIGATE TO FAVORITES TAB ==========
    print("\n[STEP 10] Navigating to Favorites tab to verify empty state...")
    home_screen.navigate_to_favorites_tab()
    time.sleep(1)  # Wait for tab transition
    print("[STEP 10] ✓ Navigated to Favorites tab")
    
    # ========== STEP 11: VERIFY NO FAVORITES MESSAGE ==========
    print("\n[STEP 11] Verifying 'No favorites yet!' message...")
    assert favorites_screen.verify_favorites_screen_displayed(), "Favorites screen did not display"
    
    # Verify that there are no favorites
    favorites_count = extended_favorites_screen.get_favorites_count()
    assert favorites_count == 0, f"Expected 0 favorites, but found {favorites_count}"
    print("[STEP 11] ✓ No favorites message verified (favorites count: 0)")
    
    print("\n[TEST] ✓ Test passed: Favorite toggle and search verification completed successfully")
