using Application.Services.Interfaces;
using Domain.Entities;
using Domain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Implementations
{
    public class CityService : ICityService
    {
        private readonly ICityRepository _cityRepository;

        #region Constructor
        public CityService(ICityRepository cityRepository)
        {
            _cityRepository = cityRepository;
        }
        #endregion
        public async Task<IEnumerable<City>> GetAllCitiesAsync()
        {
           return await _cityRepository.GetAllCitiesAsync();
        }

        public async Task<City?> GetCityByCityIdAsync(int cityId)
        {
            return await _cityRepository.GetCityByCityIdAsync(cityId);
        }
    }
}
