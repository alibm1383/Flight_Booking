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
    public class FlightRepository : IFlightRepository
    {
        private readonly FlightBookingContext _context;
         
        public FlightRepository(FlightBookingContext context)
        {
            _context = context;
        }

        public async Task AddFlightAsync(Flight flight)
        {
            await _context.Flights.AddAsync(flight);
        }

        public async Task<IEnumerable<Flight>> GetAllFlightsAsync()
        {
           return await _context.Flights.ToListAsync();
        }

        public Task<Flight?> GetFlightByIdAsync(int flightId)
        {
            return _context.Flights.FirstOrDefaultAsync(f => f.Id == flightId);
        }

        public async Task SaveChangesAsync()
        {
           await _context.SaveChangesAsync();
        }
    }
}
