import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from cryptography.exceptions import InvalidSignature

def generate_nonce() -> str:
    """Generates a cryptographically secure 32-byte challenge."""
    return base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')

def verify_signature(public_key_pem: str, nonce: str, signature_b64: str) -> bool:
    """Verifies the client's ECDSA signature, translating from WebCrypto to DER."""
    try:
        
        public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))
        
        
        padding = '=' * (-len(signature_b64) % 4)
        signature_bytes = base64.urlsafe_b64decode(signature_b64 + padding)
        
        
        if len(signature_bytes) == 64:
            r = int.from_bytes(signature_bytes[:32], 'big')
            s = int.from_bytes(signature_bytes[32:], 'big')
            der_signature = encode_dss_signature(r, s)
        else:
            der_signature = signature_bytes 
            
        
        public_key.verify(
            der_signature,
            nonce.encode('utf-8'),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except InvalidSignature:
        return False
    except Exception as e:
        print(f"Signature Verification Error: {e}")
        return False