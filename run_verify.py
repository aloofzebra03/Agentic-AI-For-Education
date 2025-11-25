import subprocess
import sys

# Run the verification script
result = subprocess.run([sys.executable, 'verify_json_structures.py'], 
                       capture_output=True, text=True, 
                       cwd='c:\\Users\\aryan\\Desktop\\Personalized_Education\\Agentic-AI-For-Education')

print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Return code:", result.returncode)
