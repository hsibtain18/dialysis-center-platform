# Add this to the very TOP of backend/app/main.py (before all other imports)

import os
import sys

print("\n" + "="*100)
print("[STARTUP-DEBUG] ALL ENVIRONMENT VARIABLES AT APPLICATION START")
print("="*100)

# Get all environment variables
all_vars = sorted(os.environ.items())

print(f"\nTotal Variables: {len(all_vars)}\n")

# Print each variable
for key, value in all_vars:
    # Hide sensitive values
    if any(sensitive in key.upper() for sensitive in ['PASSWORD', 'SECRET', 'TOKEN', 'KEY', 'CREDENTIAL']):
        display = f"{'*' * 20} (hidden, length: {len(value)})"
    else:
        # Truncate long values
        if len(value) > 100:
            display = value[:100] + f"... (truncated, total length: {len(value)})"
        else:
            display = value
    
    print(f"  {key:<40} = {display}")

print("\n" + "="*100)
print(f"[STARTUP-DEBUG] DATABASE_URL exists: {bool(os.getenv('DATABASE_URL'))}")
print(f"[STARTUP-DEBUG] RAILWAY_ENVIRONMENT_NAME: {os.getenv('RAILWAY_ENVIRONMENT_NAME', 'NOT SET')}")
print("="*100 + "\n")

# Now continue with normal imports...
# (rest of your existing main.py code below)