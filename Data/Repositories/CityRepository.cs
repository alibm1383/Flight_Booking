using Data.Context;
using Domain.Entities;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Data.Repositories
{
    public class CityRepository : ICityRepository
    {
        private readonly FlightBookingContext _context;

        #region Constructor

        public CityRepository(FlightBookingContext context)
        {
            _context = context;
        }

        #endregion

        #region City
        public async Task<IEnumerable<City>> GetAllCitiesAsync()
        {
           return await _context.Cities.ToListAsync();
        }

        public async Task<City?> GetCityByCityIdAsync(int cityId)
        {
            return await _context.Cities.FirstOrDefaultAsync(c => c.Id == cityId);
        }
        #endregion
    }
}
