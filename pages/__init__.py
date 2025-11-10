# This file makes the 'pages' directory a Python package
# and simplifies imports.

from .LoginPage import LoginPage
from .InventoryPage import InventoryPage
from .CheckoutFlowPage import (
    CartPage,
    CheckoutInfoPage,
    CheckoutOverviewPage,
    CheckoutCompletePage
)

# This allows tests to do:
# from pages import LoginPage, InventoryPage, CartPage
