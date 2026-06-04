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

namespace IOC.Dependencies
{
    public static class DependencyContainer
    {
        public static void RegisterServices(this IServiceCollection services)
        {
            #region Service
            services.AddScoped<ICityService, CityService>();
            #endregion

            #region Repository
            services.AddScoped<ICityRepository, CityRepository>();
            #endregion
        }
    }
}
