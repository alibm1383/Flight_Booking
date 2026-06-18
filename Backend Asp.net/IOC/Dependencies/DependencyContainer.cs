using Application.Services.Implementations;
using Application.Services.Interfaces;
using Domain.Interfaces;
using Microsoft.Extensions.DependencyInjection;
using Data.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Application.Profiles;

namespace IOC.Dependencies
{
    public static class DependencyContainer
    {
        public static void RegisterServices(this IServiceCollection services)
        {
            #region Service
            services.AddScoped<ICityService, CityService>();
            services.AddScoped<IAirportService, AirportService>();
            services.AddScoped<IFlightService, FlightService>();
            services.AddScoped<IFileService, FileService>();
            #endregion

            #region Repository
            services.AddScoped<ICityRepository, CityRepository>();
            services.AddScoped<IAirportReposiroty, AirportRepository>();
            services.AddScoped<IFlightRepository, FlightRepository>();
            #endregion

            #region AutoMapper
            services.AddAutoMapper(cfg => cfg.AddMaps(typeof(FlightBookingProfile).Assembly));
            #endregion
        }
    }
}
