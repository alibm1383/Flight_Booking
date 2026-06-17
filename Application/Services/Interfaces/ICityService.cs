using Domain.DTOs;
using Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Interfaces
{
    public interface ICityService
    {
        Task<IEnumerable<CityDto>> GetAllCitiesAsync();
        Task<CityDto?> GetCityByCityIdAsync(int cityId);
        Task AddCityAsync(CreateCityDto createCityDto);
    }
}
