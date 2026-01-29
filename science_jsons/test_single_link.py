import requests

url = "https://github.com/aloofzebra03/NCERT_Class7_images/blob/main/Science/English/lunar_eclipse.png"
raw_url = url.replace('/blob/', '/raw/')

print(f"Testing URL: {url}")
print(f"Raw URL: {raw_url}")
print("=" * 80)

attempts = 3
success = False

for i in range(attempts):
    print(f"\nAttempt {i+1}/{attempts}...")
    
    try:
        # Try HEAD request first
        print("  Trying HEAD request...")
        response = requests.head(raw_url, timeout=30, allow_redirects=True)
        print(f"  HEAD Response: Status {response.status_code} ({response.reason})")
        
        if response.status_code == 200:
            success = True
            print("  ✓ SUCCESS - Link is accessible!")
            break
        
        # If HEAD fails, try GET
        print("  Trying GET request...")
        response = requests.get(raw_url, timeout=30, allow_redirects=True)
        print(f"  GET Response: Status {response.status_code} ({response.reason})")
        
        if response.status_code == 200:
            success = True
            print("  ✓ SUCCESS - Link is accessible!")
            break
            
    except requests.exceptions.Timeout:
        print("  ✗ TIMEOUT - Request took too long")
    except requests.exceptions.ConnectionError as e:
        print(f"  ✗ CONNECTION ERROR - {e}")
    except Exception as e:
        print(f"  ✗ ERROR - {e}")

print("\n" + "=" * 80)
if success:
    print("FINAL RESULT: ✓ LINK IS ACCESSIBLE")
else:
    print("FINAL RESULT: ✗ LINK FAILED - May be broken, very slow, or temporarily unavailable")
