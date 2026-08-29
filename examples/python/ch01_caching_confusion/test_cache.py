import pytest
from cache_service import VulnerableCacheService, SecureSDSDCacheService

def test_vulnerable_cache_cross_tenant_leak():
    cache = VulnerableCacheService()
    # User A from Tenant 1 requests their transactions
    user_a_data = [{"id": 101, "amount": 5000, "owner": "Alice_Corp"}]
    cache.set("limit=50&offset=0", user_a_data)

    # User B from Tenant 2 requests the same query
    user_b_cached = cache.get("limit=50&offset=0")
    
    # BREACH: User B sees Alice's data!
    assert user_b_cached == user_a_data

def test_sdsd_cache_tenant_isolation_invariant():
    cache = SecureSDSDCacheService()
    user_a_data = [{"id": 101, "amount": 5000, "owner": "Alice_Corp"}]
    cache.set("tenant_1", "limit=50&offset=0", user_a_data)

    # User B from Tenant 2 makes identical query
    user_b_cached = cache.get("tenant_2", "limit=50&offset=0")

    # INVARIANT HELD: Cache miss for Tenant 2
    assert user_b_cached is None
