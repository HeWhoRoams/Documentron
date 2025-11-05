import subprocess

def run_pytest():
    subprocess.run(["python", "-m", "pytest"])

def run_xunit():
    subprocess.run(["dotnet", "test", "Documentron.Tests.csproj"])

if __name__ == "__main__":
    run_pytest()
    run_xunit()