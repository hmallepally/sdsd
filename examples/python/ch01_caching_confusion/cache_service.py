import hashlib
from typing import Optional, Dict, Any

class VulnerableCacheService:
    """Demonstrates the Syntax Trap: query-only hashing causing Cross-Tenant Cache Confusion."""
    def __init__(self):
        self.store: Dict[str, Any] = {}

    def get_cache_key(self, query_string: str) -> str:
        # VULNERABLE: Lacks tenant isolation and uses weak MD5
        return hashlib.md5(query_string.encode()).hexdigest()

    def set(self, query_string: str, data: Any):
        key = self.get_cache_key(query_string)
        self.store[key] = data

    def get(self, query_string: str) -> Optional[Any]:
        key = self.get_cache_key(query_string)
        return self.store.get(key)


class SecureSDSDCacheService:
    """SDSD Implementation: Enforces tenant isolation invariant and SHA-256."""
    def __init__(self):
        self.store: Dict[str, Any] = {}

    def get_cache_key(self, tenant_id: str, query_string: str) -> str:
        # INVARIANT: Tenant ID is strictly baked into key namespace with SHA-256
        query_hash = hashlib.sha256(query_string.encode()).hexdigest()
        return f"cache:tenant:{tenant_id}:query:{query_hash}"

    def set(self, tenant_id: str, query_string: str, data: Any):
        key = self.get_cache_key(tenant_id, query_string)
        self.store[key] = data

    def get(self, tenant_id: str, query_string: str) -> Optional[Any]:
        key = self.get_cache_key(tenant_id, query_string)
        return self.store.get(key)
