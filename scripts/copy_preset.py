import re

with open("main.js", "r") as f:
    content = f.read()

# Extract common array content
# Find "common: [" and the matching ending before "premium:"
common_match = re.search(r'common:\s*\[\s*(.*?)\s*\],\s*premium:', content, flags=re.DOTALL)
if common_match:
    common_data = common_match.group(1)
    
    # Replace the premium array
    # It starts with "premium: [" and ends before "}; \n// --- State ---"
    def replacer(m):
        return f"premium: [\n{common_data}\n    ]"
        
    new_content = re.sub(r'premium:\s*\[\s*(.*?)\s*\]', replacer, content, flags=re.DOTALL)
    
    with open("main.js", "w") as f:
        f.write(new_content)
    print("Successfully replaced premium preset with common preset.")
else:
    print("Failed to find common preset.")
