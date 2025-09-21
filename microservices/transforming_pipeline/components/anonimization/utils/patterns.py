SECRET_PATTERNS = [
    r'(?i)api[_-]?key\s*[:=]\s*[\'"]?[\w-]{16,}[\'"]?',      # API keys
    r'(?i)token\s*[:=]\s*[\'"]?[\w-]{16,}[\'"]?',            # Tokens
    r'(?i)password\s*[:=]\s*[\'"]?[\w-]{6,}[\'"]?',          # Passwords
    r'-----BEGIN [A-Z ]+ PRIVATE KEY-----[\s\S]+?-----END [A-Z ]+ PRIVATE KEY-----',  # PEM private keys
    r'AKIA[0-9A-Z]{16}',                                     # AWS Access Key ID
    r'(?i)secret[_-]?key\s*[:=]\s*[\'"]?[\w-]{16,}[\'"]?',   # Secret keys
    r'ghp_[A-Za-z0-9]{36}',                                 # GitHub Personal Access Token
    r'eyJ[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+',   # JWT tokens
    r'[A-Fa-f0-9]{64}',                                     # SHA-256 hashes
    r'[A-Fa-f0-9]{40}',                                     # SHA-1 hashes
    r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',         # MAC addresses
]

"""
Patterns for detecting secrets and sensitive information in text.

Each regex pattern is designed to match a specific type of secret, such as API keys, tokens, passwords, and cryptographic keys.
"""