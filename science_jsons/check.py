import json
import os
import requests
from pathlib import Path

def extract_github_links(json_file):
    """Extract all GitHub links from a JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    links = []
    
    def find_urls(obj, path=""):
        """Recursively find all URLs in the JSON structure."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "url" and isinstance(value, str) and "github" in value.lower():
                    links.append(value)
                else:
                    find_urls(value, f"{path}.{key}" if path else key)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                find_urls(item, f"{path}[{i}]")
    
    find_urls(data)
    return links

def check_github_link(url):
    """Check if a GitHub link is accessible."""
    try:
        # Convert blob URLs to raw URLs for better checking
        if "/blob/" in url:
            raw_url = url.replace("/blob/", "/raw/")
        else:
            raw_url = url
        
        # Send HEAD request first (faster)
        response = requests.head(raw_url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            return True, response.status_code, "OK"
        
        # If HEAD fails, try GET
        response = requests.get(raw_url, timeout=10, allow_redirects=True)
        return response.status_code == 200, response.status_code, response.reason
    except requests.exceptions.Timeout:
        return False, None, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, None, "Connection Error"
    except Exception as e:
        return False, None, str(e)

def main():
    # Get all JSON files in the science_jsons directory
    script_dir = Path(__file__).parent
    json_files = list(script_dir.glob("ch*.json"))
    
    print(f"Found {len(json_files)} JSON files\n")
    print("=" * 100)
    
    all_links = {}
    failed_links = []
    successful_links = []
    
    # Extract links from all JSON files
    for json_file in sorted(json_files):
        links = extract_github_links(json_file)
        all_links[json_file.name] = links
        print(f"\n{json_file.name}: {len(links)} GitHub links found")
    
    print("\n" + "=" * 100)
    print("\nChecking GitHub links...\n")
    
    total_links = sum(len(links) for links in all_links.values())
    checked = 0
    
    for file_name, links in all_links.items():
        for link in links:
            checked += 1
            print(f"[{checked}/{total_links}] Checking: {link[:80]}...")
            
            is_accessible, status_code, message = check_github_link(link)
            
            if is_accessible:
                successful_links.append((file_name, link, status_code))
                print(f"  ✓ SUCCESS (Status: {status_code})")
            else:
                failed_links.append((file_name, link, status_code, message))
                print(f"  ✗ FAILED (Status: {status_code}, Reason: {message})")
    
    # Summary
    print("\n" + "=" * 100)
    print("\nSUMMARY")
    print("=" * 100)
    print(f"\nTotal GitHub links found: {total_links}")
    print(f"Successful: {len(successful_links)}")
    print(f"Failed: {len(failed_links)}")
    
    if failed_links:
        print("\n" + "=" * 100)
        print("\nFAILED LINKS:")
        print("=" * 100)
        for file_name, link, status_code, message in failed_links:
            print(f"\nFile: {file_name}")
            print(f"Link: {link}")
            print(f"Status: {status_code}")
            print(f"Reason: {message}")
            print("-" * 100)
    
    if successful_links:
        print("\n" + "=" * 100)
        print("\nSUCCESSFUL LINKS (First 10):")
        print("=" * 100)
        for file_name, link, status_code in successful_links[:10]:
            print(f"\nFile: {file_name}")
            print(f"Link: {link}")
            print(f"Status: {status_code}")

if __name__ == "__main__":
    main()
