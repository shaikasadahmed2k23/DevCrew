import uuid
import datetime
from typing import Dict, List, Optional, Union

class Product:
    """
    Represents a product available in the e-commerce store.
    """
    def __init__(self, name: str, description: str, price: float, stock: int, product_id: Optional[str] = None):
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price <= 0:
            raise ValueError("Product price must be positive.")
        if stock < 0:
            raise ValueError("Product stock cannot be negative.")

        self.id: str = product_id if product_id else str(uuid.uuid4())
        self.name: str = name
        self.description: str = description
        self.price: float = price
        self.stock: int = stock

    def to_dict(self) -> Dict[str, Union[str, float, int]]:
        """Returns a dictionary representation of the product."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
        }

    def __repr__(self) -> str:
        return f"Product(id='{self.id}', name='{self.name}', price={self.price}, stock={self.stock})"


class User:
    """
    Represents a user in the system, either a customer or an admin.
    Password handling is simplified for this example.
    """
    def __init__(self, username: str, password_hash: str, role: str = 'customer', user_id: Optional[str] = None):
        if not username:
            raise ValueError("Username cannot be empty.")
        if not password_hash:
            raise ValueError("Password hash cannot be empty.")
        if role not in ['customer', 'admin']:
            raise ValueError("Invalid user role. Must be 'customer' or 'admin'.")

        self.id: str = user_id if user_id else str(uuid.uuid4())
        self.username: str = username
        self.password_hash: str = password_hash  # Simplified: stores hash directly
        self.role: str = role

    def is_admin(self) -> bool:
        """Checks if the user has admin role."""
        return self.role == 'admin'

    def to_dict(self) -> Dict[str, str]:
        """Returns a dictionary representation of the user."""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
        }

    def __repr__(self) -> str:
        return f"User(id='{self.id}', username='{self.username}', role='{self.role}')"


class CartItem:
    """
    Represents a single item (product and quantity) within a shopping cart.
    """
    def __init__(self, product_id: str, quantity: int):
        if not product_id:
            raise ValueError("Product ID cannot be empty for a cart item.")
        if quantity <= 0:
            raise ValueError("Cart item quantity must be positive.")

        self.product_id: str = product_id
        self.quantity: int = quantity

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """Returns a dictionary representation of the cart item."""
        return {
            "product_id": self.product_id,
            "quantity": self.quantity,
        }

    def __repr__(self) -> str:
        return f"CartItem(product_id='{self.product_id}', quantity={self.quantity})"


class Cart:
    """
    Represents a user's shopping cart, containing multiple CartItems.
    """
    def __init__(self, user_id: str):
        if not user_id:
            raise ValueError("User ID cannot be empty for a cart.")
        self.user_id: str = user_id
        self.items: Dict[str, CartItem] = {}  # key: product_id, value: CartItem

    def add_item(self, product_id: str, quantity: int):
        """Adds or updates an item in the cart."""
        if product_id in self.items:
            self.items[product_id].quantity += quantity
        else:
            self.items[product_id] = CartItem(product_id, quantity)

    def update_item_quantity(self, product_id: str, new_quantity: int):
        """Updates the quantity of an existing item in the cart."""
        if product_id not in self.items:
            raise ValueError(f"Product with ID '{product_id}' not found in cart.")
        if new_quantity <= 0:
            self.remove_item(product_id)
        else:
            self.items[product_id].quantity = new_quantity

    def remove_item(self, product_id: str):
        """Removes an item from the cart."""
        if product_id in self.items:
            del self.items[product_id]

    def clear(self):
        """Removes all items from the cart."""
        self.items.clear()

    def get_items(self) -> List[CartItem]:
        """Returns a list of all cart items."""
        return list(self.items.values())

    def to_dict(self) -> Dict[str, Union[str, List[Dict[str, Union[str, int]]]]]:
        """Returns a dictionary representation of the cart."""
        return {
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items.values()],
        }

    def __repr__(self) -> str:
        return f"Cart(user_id='{self.user_id}', items={len(self.items)} items)"


class OrderItem:
    """
    Represents a product item within a placed order, storing the price at the time of purchase.
    """
    def __init__(self, product_id: str, product_name: str, quantity: int, price_at_purchase: float):
        if not product_id:
            raise ValueError("Product ID cannot be empty for an order item.")
        if not product_name:
            raise ValueError("Product name cannot be empty for an order item.")
        if quantity <= 0:
            raise ValueError("Order item quantity must be positive.")
        if price_at_purchase <= 0:
            raise ValueError("Price at purchase must be positive.")

        self.product_id: str = product_id
        self.product_name: str = product_name
        self.quantity: int = quantity
        self.price_at_purchase: float = price_at_purchase

    def to_dict(self) -> Dict[str, Union[str, int, float]]:
        """Returns a dictionary representation of the order item."""
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price_at_purchase": self.price_at_purchase,
            "subtotal": self.quantity * self.price_at_purchase,
        }

    def __repr__(self) -> str:
        return (f"OrderItem(product_id='{self.product_id}', name='{self.product_name}', "
                f"quantity={self.quantity}, price_at_purchase={self.price_at_purchase})")


class Order:
    """
    Represents a placed order by a user.
    """
    def __init__(self, user_id: str, items: List[OrderItem], order_id: Optional[str] = None):
        if not user_id:
            raise ValueError("User ID cannot be empty for an order.")
        if not items:
            raise ValueError("Order must contain at least one item.")

        self.id: str = order_id if order_id else str(uuid.uuid4())
        self.user_id: str = user_id
        self.items: List[OrderItem] = items
        self.order_date: datetime.datetime = datetime.datetime.now()
        self.status: str = 'pending'  # e.g., 'pending', 'processed', 'shipped', 'delivered', 'cancelled'
        self.total_amount: float = sum(item.quantity * item.price_at_purchase for item in items)

    def to_dict(self) -> Dict[str, Union[str, float, datetime.datetime, List[Dict[str, Union[str, int, float]]]]]:
        """Returns a dictionary representation of the order."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "order_date": self.order_date.isoformat(),
            "status": self.status,
            "total_amount": self.total_amount,
            "items": [item.to_dict() for item in self.items],
        }

    def __repr__(self) -> str:
        return (f"Order(id='{self.id}', user_id='{self.user_id}', total_amount={self.total_amount}, "
                f"status='{self.status}', date={self.order_date.isoformat()})")


class ECommerceService:
    """
    Manages all core e-commerce operations including product management, user authentication,
    shopping cart interactions, and order processing.
    This class uses in-memory storage for simplicity. In a real application, this would
    interact with a database.
    """
    def __init__(self):
        self._products: Dict[str, Product] = {}
        self._users: Dict[str, User] = {}  # key: user_id
        self._users_by_username: Dict[str, User] = {} # key: username for quick lookup
        self._carts: Dict[str, Cart] = {} # key: user_id
        self._orders: Dict[str, Order] = {} # key: order_id

    def _get_user_by_id(self, user_id: str) -> Optional[User]:
        """Helper to get a user by ID."""
        return self._users.get(user_id)

    def _get_user_by_username(self, username: str) -> Optional[User]:
        """Helper to get a user by username."""
        return self._users_by_username.get(username)

    def register_user(self, username: str, password: str, role: str = 'customer') -> User:
        """
        Registers a new user in the system.
        Args:
            username: The desired username.
            password: The user's password (will be hashed in a real scenario).
            role: The role of the user, 'customer' or 'admin'. Defaults to 'customer'.
        Returns:
            The newly created User object.
        Raises:
            ValueError: If the username already exists or role is invalid.
        """
        if self._get_user_by_username(username):
            raise ValueError(f"Username '{username}' already exists.")
        
        # In a real system, 'password' would be hashed securely (e.g., using bcrypt)
        # For simplicity, we'll store it as is (or a dummy hash)
        password_hash = password # Placeholder for actual hash
        
        user = User(username=username, password_hash=password_hash, role=role)
        self._users[user.id] = user
        self._users_by_username[user.username] = user
        self._carts[user.id] = Cart(user.id) # Create an empty cart for the new user
        return user

    def login_user(self, username: str, password: str) -> User:
        """
        Logs in a user.
        Args:
            username: The user's username.
            password: The user's password.
        Returns:
            The authenticated User object.
        Raises:
            ValueError: If username or password is incorrect.
        """
        user = self._get_user_by_username(username)
        if not user or user.password_hash != password: # Simplified comparison
            raise ValueError("Invalid username or password.")
        return user

    def add_product(self, admin_user_id: str, name: str, description: str, price: float, stock: int) -> Product:
        """
        Allows an admin user to add a new product to the store.
        Args:
            admin_user_id: The ID of the admin user performing the action.
            name: The name of the product.
            description: A description of the product.
            price: The price of the product.
            stock: The initial stock quantity.
        Returns:
            The newly created Product object.
        Raises:
            ValueError: If price or stock is invalid, or if the user is not an admin.
            KeyError: If admin_user_id does not exist.
        """
        admin_user = self._get_user_by_id(admin_user_id)
        if not admin_user or not admin_user.is_admin():
            raise ValueError("Unauthorized: Only admin users can add products.")
        
        product = Product(name, description, price, stock)
        self._products[product.id] = product
        return product

    def update_product(
        self,
        admin_user_id: str,
        product_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        stock: Optional[int] = None
    ) -> Product:
        """
        Allows an admin user to update details of an existing product.
        Args:
            admin_user_id: The ID of the admin user performing the action.
            product_id: The ID of the product to update.
            name: Optional new name.
            description: Optional new description.
            price: Optional new price.
            stock: Optional new stock quantity.
        Returns:
            The updated Product object.
        Raises:
            ValueError: If the user is not an admin, or if price/stock is invalid.
            KeyError: If product_id or admin_user_id does not exist.
        """
        admin_user = self._get_user_by_id(admin_user_id)
        if not admin_user or not admin_user.is_admin():
            raise ValueError("Unauthorized: Only admin users can update products.")

        product = self._products.get(product_id)
        if not product:
            raise KeyError(f"Product with ID '{product_id}' not found.")

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            if price <= 0:
                raise ValueError("Product price must be positive.")
            product.price = price
        if stock is not None:
            if stock < 0:
                raise ValueError("Product stock cannot be negative.")
            product.stock = stock
        return product

    def delete_product(self, admin_user_id: str, product_id: str) -> None:
        """
        Allows an admin user to delete a product from the store.
        Args:
            admin_user_id: The ID of the admin user performing the action.
            product_id: The ID of the product to delete.
        Raises:
            ValueError: If the user is not an admin.
            KeyError: If product_id or admin_user_id does not exist.
        """
        admin_user = self._get_user_by_id(admin_user_id)
        if not admin_user or not admin_user.is_admin():
            raise ValueError("Unauthorized: Only admin users can delete products.")

        if product_id not in self._products:
            raise KeyError(f"Product with ID '{product_id}' not found.")
        del self._products[product_id]

    def get_all_products(self, user_id: str) -> List[Product]:
        """
        Retrieves all products in the store. Can be called by any authenticated user.
        Args:
            user_id: The ID of the user requesting the products.
        Returns:
            A list of all Product objects.
        Raises:
            KeyError: If user_id does not exist.
        """
        if user_id not in self._users:
            raise KeyError(f"User with ID '{user_id}' not found.")
        return list(self._products.values())

    def get_product_by_id(self, user_id: str, product_id: str) -> Product:
        """
        Retrieves a single product by its ID. Can be called by any authenticated user.
        Args:
            user_id: The ID of the user requesting the product.
            product_id: The ID of the product to retrieve.
        Returns:
            The Product object.
        Raises:
            KeyError: If product_id or user_id does not exist.
        """
        if user_id not in self._users:
            raise KeyError(f"User with ID '{user_id}' not found.")
        product = self._products.get(product_id)
        if not product:
            raise KeyError(f"Product with ID '{product_id}' not found.")
        return product

    def add_to_cart(self, user_id: str, product_id: str, quantity: int) -> Cart:
        """
        Adds a product to a user's shopping cart or updates its quantity.
        Args:
            user_id: The ID of the customer.
            product_id: The ID of the product to add.
            quantity: The quantity to add. Must be positive.
        Returns:
            The updated Cart object.
        Raises:
            ValueError: If quantity is not positive, user is admin, or product not found/out of stock.
            KeyError: If user_id does not exist.
        """
        user = self._get_user_by_id(user_id)
        if not user:
            raise KeyError(f"User with ID '{user_id}' not found.")
        if user.is_admin():
            raise ValueError("Admin users do not have shopping carts.")
        if quantity <= 0:
            raise ValueError("Quantity to add to cart must be positive.")

        product = self._products.get(product_id)
        if not product:
            raise ValueError(f"Product with ID '{product_id}' not found.")

        cart = self._carts[user_id]
        current_cart_quantity = cart.items[product_id].quantity if product_id in cart.items else 0
        if current_cart_quantity + quantity > product.stock:
            raise ValueError(f"Insufficient stock for product '{product.name}'. Available: {product.stock - current_cart_quantity}")

        cart.add_item(product_id, quantity)
        return cart

    def update_cart_item_quantity(self, user_id: str, product_id: str, new_quantity: int) -> Cart:
        """
        Updates the quantity of a specific product in the user's cart.
        If new_quantity is 0 or less, the item is removed.
        Args:
            user_id: The ID of the customer.
            product_id: The ID of the product in the cart.
            new_quantity: The new desired quantity.
        Returns:
            The updated Cart object.
        Raises:
            ValueError: If user is admin, product not found, or new_quantity exceeds stock.
            KeyError: If user_id or product_id not found in cart.
        """
        user = self._get_user_by_id(user_id)
        if not user:
            raise KeyError(f"User with ID '{user_id}' not found.")
        if user.is_admin():
            raise ValueError("Admin users do not have shopping carts.")
        
        cart = self._carts.get(user_id)
        if not cart:
            raise KeyError(f"Cart for user '{user_id}' not found.")

        if product_id not in cart.items:
            raise KeyError(f"Product with ID '{product_id}' not found in cart.")

        if new_quantity <= 0:
            cart.remove_item(product_id)
            return cart

        product = self._products.get(product_id)
        if not product:
            raise ValueError(f"Referenced product with ID '{product_id}' no longer exists.")

        if new_quantity > product.stock:
            raise ValueError(f"Insufficient stock for product '{product.name}'. Available: {product.stock}")

        cart.update_item_quantity(product_id, new_quantity)
        return cart

    def remove_from_cart(self, user_id: str, product_id: str) -> Cart:
        """
        Removes a product entirely from a user's shopping cart.
        Args:
            user_id: The ID of the customer.
            product_id: The ID of the product to remove.
        Returns:
            The updated Cart object.
        Raises:
            ValueError: If user is admin.
            KeyError: If user_id or product_id not found in cart.
        """
        user = self._get_user_by_id(user_id)
        if not user:
            raise KeyError(f"User with ID '{user_id}' not found.")
        if user.is_admin():
            raise ValueError("Admin users do not have shopping carts.")
        
        cart = self._carts.get(user_id)
        if not cart:
            raise KeyError(f"Cart for user '{user_id}' not found.")

        if product_id not in cart.items:
            raise KeyError(f"Product with ID '{product_id}' not found in cart.")

        cart.remove_item(product_id)
        return cart

    def get_cart(self, user_id: str) -> Cart:
        """
        Retrieves a user's current shopping cart.
        Args:
            user_id: The ID of the customer.
        Returns:
            The Cart object for the user.
        Raises:
            ValueError: If user is admin.
            KeyError: If user_id does not exist.
        """
        user = self._get_user_by_id(user_id)
        if not user:
            raise KeyError(f"User with ID '{user_id}' not found.")
        if user.is_admin():
            raise ValueError("Admin users do not have shopping carts.")
        
        return self._carts[user_id]

    def place_order(self, user_id: str) -> Order:
        """
        Places an order for the items currently in the user's cart.
        This process clears the cart and updates product stock.
        Args:
            user_id: The ID of the customer placing the order.
        Returns:
            The newly created Order object.
        Raises:
            ValueError: If user is admin, cart is empty, or insufficient stock.
            KeyError: If user_id does not exist.
        """
        user = self._get_user_by_id(user_id)
        if not user:
            raise KeyError(f"User with ID '{user_id}' not found.")
        if user.is_admin():
            raise ValueError("Admin users cannot place orders.")
        
        cart = self._carts[user_id]
        if not cart.items:
            raise ValueError("Cannot place an order with an empty cart.")

        order_items: List[OrderItem] = []
        products_to_update: Dict[str, int] = {} # product_id -> quantity to deduct

        for cart_item in cart.get_items():
            product = self._products.get(cart_item.product_id)
            if not product:
                raise ValueError(f"Product ID '{cart_item.product_id}' in cart no longer exists.")
            if product.stock < cart_item.quantity:
                raise ValueError(f"Insufficient stock for '{product.name}'. Available: {product.stock}, in cart: {cart_item.quantity}")

            order_items.append(OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=cart_item.quantity,
                price_at_purchase=product.price
            ))
            products_to_update[product.id] = cart_item.quantity

        for product_id, quantity_deduct in products_to_update.items():
            self._products[product_id].stock -= quantity_deduct

        order = Order(user_id=user_id, items=order_items)
        self._orders[order.id] = order
        cart.clear()
        return order

    def get_user_orders(self, user_id: str) -> List[Order]:
        """
        Retrieves all orders placed by a specific user.
        Args:
            user_id: The ID of the customer.
        Returns:
            A list of Order objects placed by the user.
        Raises:
            KeyError: If user_id does not exist.
        """
        user = self._get_user_by_id(user_id)
        if not user:
            raise KeyError(f"User with ID '{user_id}' not found.")
        
        return [order for order in self._orders.values() if order.user_id == user_id]

    def get_order_details(self, user_id: str, order_id: str) -> Order:
        """
        Retrieves details for a specific order, ensuring it belongs to the requesting user.
        Args:
            user_id: The ID of the user requesting order details.
            order_id: The ID of the order to retrieve.
        Returns:
            The Order object.
        Raises:
            KeyError: If user_id or order_id does not exist.
            ValueError: If the order does not belong to the user.
        """
        user = self._get_user_by_id(user_id)
        if not user:
            raise KeyError(f"User with ID '{user_id}' not found.")

        order = self._orders.get(order_id)
        if not order:
            raise KeyError(f"Order with ID '{order_id}' not found.")
        
        if not user.is_admin() and order.user_id != user_id:
            raise ValueError("Unauthorized: You can only view your own orders.")
            
        return order

    def update_order_status(self, admin_user_id: str, order_id: str, new_status: str) -> Order:
        """
        Allows an admin user to update the status of an order.
        Args:
            admin_user_id: The ID of the admin user.
            order_id: The ID of the order to update.
            new_status: The new status for the order (e.g., 'processed', 'shipped').
        Returns:
            The updated Order object.
        Raises:
            ValueError: If admin_user_id is not an admin or new_status is invalid.
            KeyError: If admin_user_id or order_id does not exist.
        """
        admin_user = self._get_user_by_id(admin_user_id)
        if not admin_user or not admin_user.is_admin():
            raise ValueError("Unauthorized: Only admin users can update order status.")

        order = self._orders.get(order_id)
        if not order:
            raise KeyError(f"Order with ID '{order_id}' not found.")
        
        valid_statuses = ['pending', 'processed', 'shipped', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid order status: '{new_status}'. Must be one of {valid_statuses}")

        order.status = new_status
        return order


# --- Example Test Cases ---
if __name__ == "__main__":
    ecommerce_service = ECommerceService()

    print("--- 1. Setup: Register Users and Add Products ---")
    try:
        admin_user = ecommerce_service.register_user("admin", "admin_pass", "admin")
        customer1 = ecommerce_service.register_user("john_doe", "john_pass")
        customer2 = ecommerce_service.register_user("jane_smith", "jane_pass")

        logged_in_admin = ecommerce_service.login_user("admin", "admin_pass")
        logged_in_customer1 = ecommerce_service.login_user("john_doe", "john_pass")
        print(f"Logged in Admin: {logged_in_admin.username}")
        print(f"Logged in Customer 1: {logged_in_customer1.username}")

        product1 = ecommerce_service.add_product(admin_user.id, "Laptop", "Powerful computing device", 1200.00, 10)
        product2 = ecommerce_service.add_product(admin_user.id, "Mouse", "Ergonomic wireless mouse", 25.50, 50)
        product3 = ecommerce_service.add_product(admin_user.id, "Keyboard", "Mechanical gaming keyboard", 75.00, 20)
        print(f"Added product: {product1.name} (Stock: {product1.stock})")
        print(f"Added product: {product2.name} (Stock: {product2.stock})")
        print(f"Added product: {product3.name} (Stock: {product3.stock})")

        all_products = ecommerce_service.get_all_products(customer1.id)
        print("\nAll Products available:")
        for p in all_products:
            print(f"- {p.name} (${p.price:.2f}) - Stock: {p.stock}")

    except ValueError as e:
        print(f"Setup Error: {e}")
    except KeyError as e:
        print(f"Setup Error: {e}")


    print("\n--- 2. Customer 1 (John Doe) Shopping Experience ---")
    try:
        ecommerce_service.add_to_cart(customer1.id, product1.id, 1)
        ecommerce_service.add_to_cart(customer1.id, product2.id, 2)
        print(f"John Doe's cart after adding items: {ecommerce_service.get_cart(customer1.id).to_dict()}")

        ecommerce_service.update_cart_item_quantity(customer1.id, product2.id, 1)
        print(f"John Doe's cart after updating mouse quantity: {ecommerce_service.get_cart(customer1.id).to_dict()}")
        
        try:
            ecommerce_service.add_to_cart(customer1.id, product1.id, 10) # 1 already in cart, stock is 10
        except ValueError as e:
            print(f"Expected error adding too many laptops: {e}")

        john_order = ecommerce_service.place_order(customer1.id)
        print(f"\nJohn Doe placed order: {john_order.to_dict()}")
        
        updated_product1 = ecommerce_service.get_product_by_id(admin_user.id, product1.id)
        updated_product2 = ecommerce_service.get_product_by_id(admin_user.id, product2.id)
        print(f"Updated stock for {updated_product1.name}: {updated_product1.stock}")
        print(f"Updated stock for {updated_product2.name}: {updated_product2.stock}")

        john_cart = ecommerce_service.get_cart(customer1.id)
        print(f"John Doe's cart after order: {john_cart.to_dict()}")
        
        john_orders = ecommerce_service.get_user_orders(customer1.id)
        print("\nJohn Doe's orders:")
        for order in john_orders:
            print(order.to_dict())

    except ValueError as e:
        print(f"John Doe's Shopping Error: {e}")
    except KeyError as e:
        print(f"John Doe's Shopping Error: {e}")


    print("\n--- 3. Admin Actions and Customer 2 (Jane Smith) Shopping ---")
    try:
        ecommerce_service.update_product(admin_user.id, product3.id, price=80.00, stock=25)
        updated_product3 = ecommerce_service.get_product_by_id(admin_user.id, product3.id)
        print(f"Admin updated {updated_product3.name}: Price ${updated_product3.price:.2f}, Stock {updated_product3.stock}")

        ecommerce_service.add_to_cart(customer2.id, product3.id, 1)
        ecommerce_service.add_to_cart(customer2.id, product1.id, 1)
        print(f"Jane Smith's cart: {ecommerce_service.get_cart(customer2.id).to_dict()}")

        print(f"\nAdmin updating status for John Doe's order: {john_order.id}")
        ecommerce_service.update_order_status(admin_user.id, john_order.id, 'shipped')
        updated_john_order = ecommerce_service.get_order_details(admin_user.id, john_order.id)
        print(f"John Doe's order status: {updated_john_order.status}")

        try:
            ecommerce_service.get_order_details(customer2.id, john_order.id)
        except ValueError as e:
            print(f"Expected error for Jane trying to view John's order: {e}")

        try:
            ecommerce_service.add_product(admin_user.id, "Invalid Item", "Test", -10.00, 5)
        except ValueError as e:
            print(f"Expected error adding product with invalid price: {e}")

    except ValueError as e:
        print(f"Admin/Jane Smith Shopping Error: {e}")
    except KeyError as e:
        print(f"Admin/Jane Smith Shopping Error: {e}")