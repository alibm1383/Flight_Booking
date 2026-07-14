using Data.Context;
using Domain.DTOs;
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

        public async Task<PagedResult<Flight>> SearchAsync(SearchFlightDto searchFlightDto)
        {
            DateTime startDate;
            DateTime endDate;
            if (searchFlightDto.FromTime == null)
            {
                startDate = DateTime.SpecifyKind(searchFlightDto.DepartureDate.ToDateTime(TimeOnly.MinValue),DateTimeKind.Utc);
            }
            else
            {
                startDate = DateTime.SpecifyKind(searchFlightDto.DepartureDate.ToDateTime(searchFlightDto.FromTime.Value),DateTimeKind.Utc);
            }
            
            if (searchFlightDto.ToTime == null)
            {
                endDate = DateTime.SpecifyKind(searchFlightDto.DepartureDate.ToDateTime(TimeOnly.MinValue).AddDays(1),DateTimeKind.Utc);
            }
            else
            {
                endDate = DateTime.SpecifyKind(searchFlightDto.DepartureDate.ToDateTime(searchFlightDto.ToTime.Value),DateTimeKind.Utc);
            }


            var query = _context.Flights
                .Where(f => f.SourceId == searchFlightDto.SourceId)
                .Where(f => f.DestinationId == searchFlightDto.DestinationId)
                .Where(f => f.DepartureTime >= startDate && f.DepartureTime <= endDate);

            if (searchFlightDto.MinPrice.HasValue)
            {
                query = query.Where(f => f.Price >= searchFlightDto.MinPrice);
            }
            if (searchFlightDto.MaxPrice.HasValue)
            {
                query = query.Where(f => f.Price <= searchFlightDto.MaxPrice);
            }

            if (searchFlightDto.AirlineId.HasValue)
            {
                query = query.Where(f => f.AirlineId == searchFlightDto.AirlineId);
            }

            switch (searchFlightDto.SortBy)
            {
                case FlightSortBy.PriceAsc:
                    query = query.OrderBy(f => f.Price);
                    break;
                case FlightSortBy.TimeAsc:
                    query = query.OrderBy(f => f.DepartureTime);
                    break;
            }

            int totalCount = await query.CountAsync();
            var flights =  await query.Skip((searchFlightDto.PageNumber-1) * searchFlightDto.PageSize)
                .Take(searchFlightDto.PageSize).ToListAsync();
            return new PagedResult<Flight>()
            {
                Items = flights,
                TotalCount = totalCount,
                PageSize = searchFlightDto.PageSize,
                PageNumber = searchFlightDto.PageNumber
            };
        }

        public Task<Flight?> GetFlightByIdAsync(int flightId)
        {
            return _context.Flights.FirstOrDefaultAsync(f => f.Id == flightId);
        }

        public async Task SaveChangesAsync()
        {
            await _context.SaveChangesAsync();
        }

        public async Task<IEnumerable<Flight>> GetFlightsByAirlineIdAsync(int airlineId)
        {
            return await _context.Flights.AsNoTracking()
                .Where(f => f.AirlineId == airlineId)
                .OrderBy(f => f.DepartureTime).ToListAsync();
        }

        public async Task<IEnumerable<Passenger>> GetPassengersByFlightIdAsync(int flightId)
        {
            return await _context.Passengers
                .Where(p => p.Booking.FlightId == flightId).ToListAsync();
        }
    }
}
