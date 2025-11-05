using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using System.Text.Json;

class ApiProgram
{
    static void Main(string[] args)
    {
        var app = WebApplication.Create();

        app.MapPost("/inspect", async (HttpContext context) =>
        {
            // Implement analysis similar to CLI
            // For now, return ok
            return Results.Ok(new { build_info = "path", symbol_graph = "path", api_surface = "path", deps_map = "path", quality_report = "path" });
        });

        app.Run();
    }
}