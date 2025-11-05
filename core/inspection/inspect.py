import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python inspect.py <repo_path>")
        return
    repo_path = sys.argv[1]
    # Call C# analyzer
    result = subprocess.run(["dotnet", "run", "--project", "Documentron/adapters/csharp/Documentron.Adapters.CSharp.csproj", repo_path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)

if __name__ == "__main__":
    main()