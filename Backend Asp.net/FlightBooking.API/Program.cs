using Data.Context;
using IOC.Dependencies;
using Microsoft.EntityFrameworkCore;
var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();

builder.Services.RegisterServices();
#region AddDbContext

builder.Services.AddDbContext<FlightBookingContext>(options =>
{
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection"));
});

#endregion

// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy
            .AllowAnyHeader()
            .AllowAnyMethod()
            .WithOrigins(
                "http://localhost:3000",   // python/node local server
                "http://localhost:5173",   // Vue dev server
                "http://127.0.0.1:3000",
                "http://127.0.0.1:5173"
            );
    });
});

var app = builder.Build();

// Configure the HTTP request pipeline.


if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseCors("AllowAll");

app.UseStaticFiles();

app.UseAuthorization();

app.MapControllers();

app.Run();
