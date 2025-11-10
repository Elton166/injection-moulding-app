"""
Serializers for the eCommerce store API.

This module contains all the serializers for converting model instances
to JSON and handling API request/response data.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Store, Product, Review, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'user_type', 'phone', 'address', 'created_at']
        read_only_fields = ['created_at']


class StoreListSerializer(serializers.ModelSerializer):
    """Serializer for Store model in list views."""
    vendor = UserSerializer(read_only=True)
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = [
            'id', 'name', 'description', 'address', 'phone', 'email',
            'vendor', 'is_active', 'created_at', 'product_count'
        ]
        read_only_fields = ['id', 'created_at', 'vendor']
    
    def get_product_count(self, obj):
        """Get the number of active products in the store."""
        return obj.product_set.filter(is_active=True).count()


class StoreDetailSerializer(serializers.ModelSerializer):
    """Serializer for Store model in detail views."""
    vendor = UserSerializer(read_only=True)
    products = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = [
            'id', 'name', 'description', 'address', 'phone', 'email',
            'vendor', 'is_active', 'created_at', 'products'
        ]
        read_only_fields = ['id', 'created_at', 'vendor']
    
    def get_products(self, obj):
        """Get active products for this store."""
        products = obj.product_set.filter(is_active=True)[:10]  # Limit to 10
        return ProductListSerializer(products, many=True, context=self.context).data


class StoreCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Store instances."""
    
    class Meta:
        model = Store
        fields = [
            'name', 'description', 'address', 'phone', 'email'
        ]
    
    def create(self, validated_data):
        """Create a new store with the current user as vendor."""
        validated_data['vendor'] = self.context['request'].user
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for Product model in list views."""
    store = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock_quantity',
            'image', 'store', 'is_active', 'created_at',
            'average_rating', 'review_count'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_store(self, obj):
        """Get store information."""
        return {
            'id': obj.store.id,
            'name': obj.store.name,
            'vendor': obj.store.vendor.username
        }
    
    def get_average_rating(self, obj):
        """Calculate average rating for the product."""
        reviews = obj.review_set.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0.0
    
    def get_review_count(self, obj):
        """Get the number of reviews for the product."""
        return obj.review_set.count()


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for Product model in detail views."""
    store = StoreListSerializer(read_only=True)
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock_quantity',
            'image', 'store', 'is_active', 'created_at',
            'reviews', 'average_rating'
        ]
        read_only_fields = ['id', 'created_at', 'store']
    
    def get_reviews(self, obj):
        """Get recent reviews for this product."""
        reviews = obj.review_set.all().order_by('-created_at')[:5]  # Latest 5
        return ReviewSerializer(reviews, many=True, context=self.context).data
    
    def get_average_rating(self, obj):
        """Calculate average rating for the product."""
        reviews = obj.review_set.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 1)
        return 0.0


class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Product instances."""
    store_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'stock_quantity',
            'image', 'store_id'
        ]
    
    def validate_store_id(self, value):
        """Validate that the store exists and belongs to the current user."""
        try:
            store = Store.objects.get(id=value)
            if store.vendor != self.context['request'].user:
                raise serializers.ValidationError(
                    "You can only add products to your own stores."
                )
            return value
        except Store.DoesNotExist:
            raise serializers.ValidationError("Store does not exist.")
    
    def create(self, validated_data):
        """Create a new product."""
        store_id = validated_data.pop('store_id')
        store = Store.objects.get(id=store_id)
        validated_data['store'] = store
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user = UserSerializer(read_only=True)
    product = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'product', 'user', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'user']
    
    def get_product(self, obj):
        """Get product information."""
        return {
            'id': obj.product.id,
            'name': obj.product.name
        }


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Review instances."""
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5."""
        if not 1 <= value <= 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )
        return value
    
    def create(self, validated_data):
        """Create a new review."""
        # customer and product are passed via perform_create in the view
        return super().create(validated_data)


class VendorStoreSerializer(serializers.ModelSerializer):
    """Serializer for vendor's own stores."""
    product_count = serializers.SerializerMethodField()
    total_revenue = serializers.SerializerMethodField()
    
    class Meta:
        model = Store
        fields = [
            'id', 'name', 'description', 'address', 'phone', 'email',
            'is_active', 'created_at', 'product_count', 'total_revenue'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_product_count(self, obj):
        """Get the number of products in the store."""
        return obj.product_set.count()
    
    def get_total_revenue(self, obj):
        """Calculate total revenue (placeholder for future implementation)."""
        # This would be calculated from actual orders in a real implementation
        return 0.00