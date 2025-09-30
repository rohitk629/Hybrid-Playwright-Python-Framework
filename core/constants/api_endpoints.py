"""
API Endpoints Constants
"""


class APIEndpoints:
    """API endpoint constants"""

    # User Endpoints
    USER_BASE = "/users"
    USER_CREATE = "/users"
    USER_GET_BY_ID = "/users/{user_id}"
    USER_UPDATE = "/users/{user_id}"
    USER_DELETE = "/users/{user_id}"
    USER_LIST = "/users"
    USER_SEARCH = "/users/search"

    # Product Endpoints
    PRODUCT_BASE = "/products"
    PRODUCT_CREATE = "/products"
    PRODUCT_GET_BY_ID = "/products/{product_id}"
    PRODUCT_UPDATE = "/products/{product_id}"
    PRODUCT_DELETE = "/products/{product_id}"
    PRODUCT_LIST = "/products"
    PRODUCT_SEARCH = "/products/search"

    # Order Endpoints
    ORDER_BASE = "/orders"
    ORDER_CREATE = "/orders"
    ORDER_GET_BY_ID = "/orders/{order_id}"
    ORDER_UPDATE = "/orders/{order_id}"
    ORDER_DELETE = "/orders/{order_id}"
    ORDER_LIST = "/orders"
    ORDER_BY_USER = "/orders/user/{user_id}"

    # Authentication Endpoints
    AUTH_LOGIN = "/auth/login"
    AUTH_LOGOUT = "/auth/logout"
    AUTH_REGISTER = "/auth/register"
    AUTH_REFRESH_TOKEN = "/auth/refresh"
    AUTH_FORGOT_PASSWORD = "/auth/forgot-password"
    AUTH_RESET_PASSWORD = "/auth/reset-password"