from django.core.handlers.wsgi import WSGIRequest


class Cart:
    def __init__(self, request: WSGIRequest) -> None:
        self.__session = request.session
        self.__cart = self.__session.get("cart")

        if self.__cart is None:
            self.__cart: list = []
            self.__session["cart"] = self.__cart
    
    @property
    def cart(self) -> list[int]:
        return self.__cart
    
    def add(self, product_id: int) -> None:
        if product_id not in self.__cart:
            self.__cart.append(product_id)
            self.save()
    
    def remove(self, product_id: int) -> None:
        if product_id in self.__cart:
            self.__cart.remove(product_id)
            self.save()
    
    def clear(self) -> None:
        if "cart" in self.__session:
            del self.__session["cart"]
        
        self.__cart = []
        self.save()
    
    def save(self) -> None:
        self.__session.modified = True

    def __len__(self) -> int:
        return len(self.__cart)
