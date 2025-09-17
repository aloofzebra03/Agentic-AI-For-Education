"""
LangSmith Projects Listing Tool
This script lists all your LangSmith projects with URLs and trace counts.
"""

import os
from dotenv import load_dotenv
from datetime import datetime

def list_langsmith_projects():
    """List all LangSmith projects with URLs and trace counts."""
    
    # Load environment variables
    load_dotenv(dotenv_path=".env", override=True)
    
    # Set up LangSmith connection
    langsmith_key = os.getenv('LANGCHAIN_API_KEY')
    print(langsmith_key)
    if not langsmith_key:
        print("❌ LANGSMITH_API_KEY not found in .env file")
        return
    
    os.environ['LANGCHAIN_API_KEY'] = langsmith_key
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    
    try:
        from langsmith import Client
        client = Client()
        
        print("🔍 FETCHING YOUR LANGSMITH PROJECTS...")
        print("=" * 80)
        print()
        
        # Get all projects
        projects = list(client.list_projects())
        
        if not projects:
            print("❌ No projects found in your LangSmith workspace")
            return
        
        print(f"📊 Found {len(projects)} project(s) in your workspace:")
        print()
        
        for i, project in enumerate(projects, 1):
            try:
                # Get runs count for each project
                runs = list(client.list_runs(project_name=project.name, limit=100))
                run_count = len(runs)
                
                # Get recent run info
                recent_run_info = ""
                if runs:
                    latest_run = runs[0]
                    recent_run_info = f" (Latest: {latest_run.start_time.strftime('%Y-%m-%d %H:%M')})"
                
                # Generate project URL
                project_url = f"https://smith.langchain.com/projects/p/{project.id}"
                
                print(f"📁 PROJECT {i}: {project.name}")
                print(f"   🆔 ID: {project.id}")
                print(f"   🔗 URL: {project_url}")
                print(f"   📊 Traces: {run_count}{recent_run_info}")
                print()
                
            except Exception as e:
                print(f"   ❌ Error fetching runs for {project.name}: {str(e)}")
                project_url = f"https://smith.langchain.com/projects/p/{project.id}"
                print(f"   🔗 URL: {project_url}")
                print(f"   📊 Traces: Unable to fetch")
                print()
        
        print("=" * 80)
        print("💡 TIPS:")
        print("• Click any URL above to open that project in LangSmith")
        print("• If a project shows 'One or more sessions not found', try a different project")
        print("• Projects with recent traces are more likely to display correctly")
        print()
        print("🔄 To refresh this list, run this script again")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error connecting to LangSmith: {e}")
        print()
        print("Possible solutions:")
        print("1. Check your LANGSMITH_API_KEY in the .env file")
        print("2. Verify internet connection")
        print("3. Check if LangSmith service is available")

def main():
    """Main function."""
    print(f"🚀 LangSmith Projects List - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    list_langsmith_projects()

if __name__ == "__main__":
    main()
