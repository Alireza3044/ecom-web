from django.core.handlers.wsgi import WSGIRequest


class Cart:
    def __init__(self, request: WSGIRequest) -> None:
        self.session = request.session

        self.cart = self.session.get("cart")
        if self.cart is None:
            self.cart = {}
            self.session["cart"] = self.cart
    
    def get_cart(self) -> None:
        return self.cart
    
    def add(self, product_id: int | str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
        
        self.cart[product_id]["quantity"] += quantity
        self.save()
    
    def reduce(self, product_id: int | str) -> None:
        product_id = str(product_id)
        if product_id in self.cart:
            quantity = self.cart[product_id]["quantity"]
            if quantity > 1:
                self.cart[product_id]["quantity"] = quantity - 1
            else:
                del self.cart[product_id]
            
            self.save()
    
    def remove(self, product_id: int | str) -> None:
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def clear(self) -> None:
        if "cart" in self.session:
            del self.session["cart"]
        
        self.cart = {}
        self.save()
    
    def save(self) -> None:
        self.session.modified = True

    def __len__(self) -> None:
        return sum(item["quantity"] for item in self.cart.values())
