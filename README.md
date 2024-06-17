# SsPassword

## Installation

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Generate a secret key by executing:

```python
from app.encryption import generate_key, save_key
key = generate_key()
save_key(key)
```
