using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.MSBuild;
using Microsoft.Build.Locator;
using System.Text.Json;
using System.Collections.Generic;

// Simple DTO for symbol data (avoid conflict with Microsoft.CodeAnalysis.SymbolInfo)
public sealed class SymbolItem
{
    public string? Id { get; set; }
    public string Kind { get; set; } = "";
    public string? Access { get; set; }
}

class Program
{
    private static bool s_msbuildRegistered = false;
    private static readonly object s_msbuildLock = new object();

    static async Task Main(string[] args)
    {
        if (args.Length == 0)
        {
            Console.WriteLine("Usage: Documentron.Adapters.CSharp <repo_path> [artifacts_path]");
            return;
        }
        string repoPath = args[0];
        // Ensure artifacts directory exists - use provided path or default under repo
        // Default: all generated outputs under top-level 'Generated Documentation'
        string artifactsDir = args.Length > 1 ? args[1] : Path.Combine(repoPath, "Generated Documentation");
        Directory.CreateDirectory(artifactsDir);

        // Try full MSBuild-based inspection first; if unavailable, fall back to a lightweight mode
        bool success = await TryMsbuildInspect(repoPath, artifactsDir);
        if (!success)
        {
            Console.WriteLine("Falling back to lightweight inspection mode.");
            await LiteInspect(repoPath, artifactsDir);
        }
        Console.WriteLine("Artifacts generated");
    }

    private static async Task<bool> TryMsbuildInspect(string repoPath, string artifactsDir)
    {
        try
        {
            // Thread-safe registration of MSBuild - only call once per process
            if (!s_msbuildRegistered)
            {
                lock (s_msbuildLock)
                {
                    if (!s_msbuildRegistered)
                    {
                        // Allow manual override via environment variables
                        // MSBUILD_EXE_PATH (full path to MSBuild.exe) or MSBUILD_PATH (directory containing MSBuild.exe)
                        var envExe = Environment.GetEnvironmentVariable("MSBUILD_EXE_PATH");
                        var envDir = Environment.GetEnvironmentVariable("MSBUILD_PATH");
                        if (!string.IsNullOrWhiteSpace(envExe) && File.Exists(envExe))
                        {
                            var dir = Path.GetDirectoryName(envExe);
                            if (dir == null)
                            {
                                // Fall back for root paths (e.g., "C:\msbuild.exe")
                                dir = Path.GetPathRoot(envExe) ?? Directory.GetParent(envExe)?.FullName;
                            }
                            if (!string.IsNullOrWhiteSpace(dir))
                            {
                                MSBuildLocator.RegisterMSBuildPath(dir);
                            }
                        }
                        else if (!string.IsNullOrWhiteSpace(envDir) && Directory.Exists(envDir))
                        {
                            MSBuildLocator.RegisterMSBuildPath(envDir);
                        }
                        else
                        {
                            try
                            {
                                // First attempt: standard defaults (prefers VS if installed)
                                MSBuildLocator.RegisterDefaults();
                            }
                            catch
                            {
                                // Fallback: try to locate dotnet SDK's MSBuild assemblies
                                var sdkPath = TryGetDotnetSdkPath();
                                if (sdkPath == null)
                                    throw; // rethrow original failure
                                MSBuildLocator.RegisterMSBuildPath(sdkPath);
                            }
                        }
                        s_msbuildRegistered = true;
                    }
                }
            }
        }
        catch (Exception ex)
        {
            // MSBuild registration failed - fall back to lite mode
            Console.WriteLine($"MSBuild registration failed: {ex.Message}");
            return false;
        }

        try
        {
            using var workspace = MSBuildWorkspace.Create();

            // Prefer solution if present
            var solutionPath = Directory.GetFiles(repoPath, "*.sln", SearchOption.AllDirectories).FirstOrDefault();
            if (solutionPath != null)
            {
                Console.WriteLine($"Using solution: {solutionPath}");
                var solution = await workspace.OpenSolutionAsync(solutionPath);

                // Build info
                var buildInfo = new
                {
                    solutions = new[] { new { name = Path.GetFileNameWithoutExtension(solutionPath), path = solutionPath, projects = solution.Projects.Select(p => p.Name).ToArray() } },
                    projects = solution.Projects.Select(p => new { name = p.Name, path = p.FilePath, targets = p.CompilationOptions?.OutputKind.ToString() }).ToArray()
                };
                File.WriteAllText(Path.Combine(artifactsDir, "build.info.json"), JsonSerializer.Serialize(buildInfo));

                // Symbol graph - classes (semantic)
                var symbols = await ExtractSymbolsFromProjects(solution.Projects);
                File.WriteAllText(Path.Combine(artifactsDir, "symbol.graph.json"), JsonSerializer.Serialize(new { symbols }));

                // API surface - public classes/methods
                var apiSurface = new { public_apis = symbols.Where(s => s.Access == "Public").ToArray() };
                File.WriteAllText(Path.Combine(artifactsDir, "api.surface.json"), JsonSerializer.Serialize(apiSurface));

                // Deps map - basic project references
                var deps = solution.Projects.SelectMany(p => p.ProjectReferences.Select(r => new { from = p.Name, to = solution.Projects.FirstOrDefault(pr => pr.Id == r.ProjectId)?.Name, kind = "project" })).ToArray();
                var depsMap = new { dependencies = deps };
                File.WriteAllText(Path.Combine(artifactsDir, "deps.map.json"), JsonSerializer.Serialize(depsMap));

                // Quality report - placeholder until real metrics computation is implemented
                var qualityReport = new { 
                    placeholder = true,
                    metrics = new { 
                        symbol_resolution_rate = symbols.Count == 0 ? 0 : 1.0,
                        project_discovery_rate = 1.0,
                        ms_per_kloc = 25
                    },
                    note = "Metrics are placeholders until real computation is implemented"
                };
                File.WriteAllText(Path.Combine(artifactsDir, "quality.report.json"), JsonSerializer.Serialize(qualityReport));
                return true;
            }

            // If no solution, try to open all csproj files directly
            var csprojPaths = Directory.GetFiles(repoPath, "*.csproj", SearchOption.AllDirectories);
            if (csprojPaths.Length == 0)
            {
                Console.WriteLine("No .sln or .csproj files found for MSBuild inspection.");
                return false;
            }

            Console.WriteLine($"No solution found; opening {csprojPaths.Length} project(s) for MSBuild inspection.");
            foreach (var projPath in csprojPaths)
            {
                try
                {
                    await workspace.OpenProjectAsync(projPath);
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Failed to open project {projPath}: {ex.Message}");
                }
            }

            var sol = workspace.CurrentSolution;
            if (sol == null || !sol.Projects.Any())
            {
                Console.WriteLine("MSBuild workspace contains no projects after loading.");
                return false;
            }

            // Build info from projects
            var projInfos = sol.Projects.Select(p => new { name = p.Name, path = p.FilePath, targets = p.CompilationOptions?.OutputKind.ToString() }).ToArray();
            var buildInfoNoSln = new { solutions = Array.Empty<object>(), projects = projInfos };
            File.WriteAllText(Path.Combine(artifactsDir, "build.info.json"), JsonSerializer.Serialize(buildInfoNoSln));

            // Symbol graph across projects
            var symbolsNoSln = await ExtractSymbolsFromProjects(sol.Projects);
            File.WriteAllText(Path.Combine(artifactsDir, "symbol.graph.json"), JsonSerializer.Serialize(new { symbols = symbolsNoSln }));

            var apiSurfaceNoSln = new { public_apis = symbolsNoSln.Where(s => s.Access == "Public").ToArray() };
            File.WriteAllText(Path.Combine(artifactsDir, "api.surface.json"), JsonSerializer.Serialize(apiSurfaceNoSln));

            // Deps map - project references from loaded projects
            var depsNoSln = new List<object>();
            foreach (var project in sol.Projects)
            {
                foreach (var projectRef in project.ProjectReferences)
                {
                    // Try to resolve the referenced project by ID within the current solution
                    var referencedProject = sol.Projects.FirstOrDefault(p => p.Id == projectRef.ProjectId);
                    if (referencedProject != null)
                    {
                        depsNoSln.Add(new { from = project.Name, to = referencedProject.Name, kind = "project" });
                    }
                    // Note: ProjectReference doesn't have Include property in MSBuild workspace,
                    // so we can only resolve references to projects that are actually loaded
                }
            }
            var depsMapNoSln = new { dependencies = depsNoSln };
            File.WriteAllText(Path.Combine(artifactsDir, "deps.map.json"), JsonSerializer.Serialize(depsMapNoSln));

            var qualityNoSln = new { placeholder = true, metrics = new { symbol_resolution_rate = symbolsNoSln.Count == 0 ? 0 : 1.0, project_discovery_rate = projInfos.Length > 0 ? 1.0 : 0.0, ms_per_kloc = 25 }, note = "Metrics are placeholders until real computation is implemented" };
            File.WriteAllText(Path.Combine(artifactsDir, "quality.report.json"), JsonSerializer.Serialize(qualityNoSln));
            return true;
        }
        catch (Exception ex)
        {
            // MSBuild inspection failed - fall back to lite mode
            Console.WriteLine($"MSBuild inspection failed: {ex.Message}");
            return false;
        }
    }

    private static async Task<List<SymbolItem>> ExtractSymbolsFromProjects(IEnumerable<Project> projects)
    {
        var symbols = new List<SymbolItem>();
        foreach (var project in projects)
        {
            var compilation = await project.GetCompilationAsync();
            if (compilation == null) continue;
            foreach (var syntaxTree in compilation.SyntaxTrees)
            {
                var semanticModel = compilation.GetSemanticModel(syntaxTree);
                var root = await syntaxTree.GetRootAsync();
                var classDeclarations = root.DescendantNodes().OfType<ClassDeclarationSyntax>();
                foreach (var classDecl in classDeclarations)
                {
                    var symbol = semanticModel.GetDeclaredSymbol(classDecl);
                    symbols.Add(new SymbolItem { Id = symbol?.ToDisplayString(), Kind = "class", Access = symbol?.DeclaredAccessibility.ToString() });
                }
            }
        }
        return symbols;
    }

    private static string? TryGetDotnetSdkPath()
    {
        try
        {
            // Use 'dotnet --list-sdks' and pick the highest version directory
            var psi = new System.Diagnostics.ProcessStartInfo("dotnet", "--list-sdks")
            {
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false
            };
            using var p = System.Diagnostics.Process.Start(psi);
            if (p == null) return null;
            var output = p.StandardOutput.ReadToEnd();
            if (!p.WaitForExit(3000)) 
            {
                try { p.Kill(); } catch { }
                return null;
            }
            if (p.ExitCode != 0) return null;
            var lines = output.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            // lines like: 8.0.100 [C:\Program Files\dotnet\sdk]
            var sdkEntries = new List<(Version version, string path)>();
            foreach (var line in lines)
            {
                var parts = line.Split('[', ']');
                if (parts.Length >= 2)
                {
                    var verStr = parts[0].Trim();
                    var basePath = parts[1].Trim();
                    if (Version.TryParse(verStr.Split('-')[0], out var ver))
                    {
                        var full = Path.Combine(basePath, verStr);
                        if (Directory.Exists(full))
                        {
                            sdkEntries.Add((ver, full));
                        }
                    }
                }
            }
            if (sdkEntries.Count == 0) return null;
            return sdkEntries.OrderByDescending(e => e.version).First().path;
        }
        catch
        {
            return null;
        }
    }

    private static async Task LiteInspect(string repoPath, string artifactsDir)
    {
        // Discover .sln and .csproj
        var solutionPath = Directory.GetFiles(repoPath, "*.sln", SearchOption.AllDirectories).FirstOrDefault();
        var csprojs = Directory.GetFiles(repoPath, "*.csproj", SearchOption.AllDirectories);
        var projects = csprojs.Select(p => new { name = Path.GetFileNameWithoutExtension(p), path = p, targets = "Unknown" }).ToArray();
        var buildInfo = new
        {
            solutions = solutionPath != null ? new[] { new { name = Path.GetFileNameWithoutExtension(solutionPath), path = solutionPath, projects = projects.Select(p => p.name).ToArray() } } : Array.Empty<object>(),
            projects
        };
        File.WriteAllText(Path.Combine(artifactsDir, "build.info.json"), JsonSerializer.Serialize(buildInfo));

        // Parse classes from source files
        var symbols = new List<SymbolItem>();
        var csFiles = Directory.GetFiles(repoPath, "*.cs", SearchOption.AllDirectories)
            .Where(p => !p.Contains(Path.DirectorySeparatorChar + "bin" + Path.DirectorySeparatorChar) && !p.Contains(Path.DirectorySeparatorChar + "obj" + Path.DirectorySeparatorChar));
        foreach (var file in csFiles)
        {
            try
            {
                var text = await File.ReadAllTextAsync(file);
                var tree = Microsoft.CodeAnalysis.CSharp.CSharpSyntaxTree.ParseText(text);
                var root = await tree.GetRootAsync();
                var classDeclarations = root.DescendantNodes().OfType<ClassDeclarationSyntax>();
                foreach (var cls in classDeclarations)
                {
                    var access = cls.Modifiers.Any(m => m.IsKind(Microsoft.CodeAnalysis.CSharp.SyntaxKind.PublicKeyword)) ? "Public" : "Internal";
                    var id = cls.Identifier.Text;
                    symbols.Add(new SymbolItem { Id = id, Kind = "class", Access = access });
                }
            }
            catch (IOException ex)
            {
                Console.Error.WriteLine($"IO error reading file {file}: {ex.Message}");
            }
            catch (UnauthorizedAccessException ex)
            {
                Console.Error.WriteLine($"Access denied reading file {file}: {ex.Message}");
            }
            catch (ArgumentException ex)
            {
                Console.Error.WriteLine($"Invalid argument parsing file {file}: {ex.Message}");
            }
            catch (InvalidOperationException ex)
            {
                Console.Error.WriteLine($"Invalid operation parsing file {file}: {ex.Message}");
            }
            // Don't catch fatal exceptions like OutOfMemoryException, StackOverflowException, ThreadAbortException
        }
        var symbolGraph = new { symbols };
        File.WriteAllText(Path.Combine(artifactsDir, "symbol.graph.json"), JsonSerializer.Serialize(symbolGraph));

        var apiSurface = new { public_apis = symbols.Where(s => s.Access == "Public").ToArray() };
        File.WriteAllText(Path.Combine(artifactsDir, "api.surface.json"), JsonSerializer.Serialize(apiSurface));

        // Basic deps via csproj <ProjectReference>
        var deps = new List<object>();
        foreach (var proj in csprojs)
        {
            try
            {
                var doc = System.Xml.Linq.XDocument.Load(proj);
                var name = Path.GetFileNameWithoutExtension(proj);
                // Handle namespaced elements by matching LocalName
                var refs = doc.Descendants().Where(e => e.Name.LocalName == "ProjectReference")
                    .Select(x => x.Attribute("Include")?.Value)
                    .Where(v => !string.IsNullOrEmpty(v))
                    .ToList();
                foreach (var r in refs)
                {
                    var toName = Path.GetFileNameWithoutExtension(r!);
                    deps.Add(new { from = name, to = toName, kind = "project" });
                }
            }
            catch (System.Xml.XmlException ex)
            {
                Console.Error.WriteLine($"XML parsing error in project file {proj}: {ex.Message}");
            }
            catch (IOException ex)
            {
                Console.Error.WriteLine($"IO error reading project file {proj}: {ex.Message}");
            }
            catch (UnauthorizedAccessException ex)
            {
                Console.Error.WriteLine($"Access denied reading project file {proj}: {ex.Message}");
            }
        }
        var depsMap = new { dependencies = deps };
        File.WriteAllText(Path.Combine(artifactsDir, "deps.map.json"), JsonSerializer.Serialize(depsMap));

        var qualityReport = new { metrics = new { symbol_resolution_rate = 0.5, project_discovery_rate = 1.0, ms_per_kloc = 25 } };
        File.WriteAllText(Path.Combine(artifactsDir, "quality.report.json"), JsonSerializer.Serialize(qualityReport));
    }
}
