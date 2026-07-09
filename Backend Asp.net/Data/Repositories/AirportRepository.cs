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
    public class AirportRepository : IAirportRepository
    {
        private readonly FlightBookingContext _context;
        public AirportRepository(FlightBookingContext context)
        {
            _context = context;
        }
        public async Task AddAirportAsync(Airport airport)
        {
           await _context.Airports.AddAsync(airport);
        }

        public async Task<Airport?> GetAirportByIdAsync(int airportId)
        {
            return await _context.Airports.FirstOrDefaultAsync(a => a.Id == airportId);
        }

        public async Task<IEnumerable<Airport>> GetAllAirportsAsync()
        {
            return await _context.Airports.ToListAsync();
        }

        public async Task SaveChangesAsync()
        {
            await _context.SaveChangesAsync();
        }
    }
}
