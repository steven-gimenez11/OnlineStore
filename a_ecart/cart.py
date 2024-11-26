from a_store.models import Product

class Cart:
    
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key', {})
        
        if 'session_key' not in request.session:
            self.session['session_key'] = {}
        
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = product.id
        product_qty = str(quantity)
        
        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            pass
    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        if product_id not in self.cart:
            self.cart[product_id] = int(product_qty)
        
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            pass
        
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for key, value in self.cart.items():
            key = str(key)
            for product in products:
                if product.id == key:
                    total += product.price * value
        return total
        
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quantities(self):
        return self.cart
    
    def get_product_totals(self):
        product_totals = {}
        for product_id, quantity in self.cart.items():
            product = Product.objects.get(id=product_id)
            product_totals[product_id] = product.price * quantity
        return product_totals

    def update(self, product, quantity):
        """Actualiza la cantidad de un producto en el carrito"""
        product_id = str(product.id) 
        product_qty = int(quantity) 

        if product_id in self.cart:
            self.cart[product_id] = product_qty 

        self.session.modified = True

        if self.request.user.is_authenticated:
            pass

        return self.cart
    
    def delete(self, product):
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            pass
