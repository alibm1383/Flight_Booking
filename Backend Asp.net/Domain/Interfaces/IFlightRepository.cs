using Domain.DTOs;
using Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Interfaces
{
    public interface IFlightRepository
    {
        Task<PagedResult<Flight>> SearchAsync(SearchFlightDto searchFlightDto);
        Task<Flight?> GetFlightByIdAsync(int flightId);
        Task<IEnumerable<Flight>> GetFlightsByAirlineIdAsync(int airlineId);
        Task<IEnumerable<Passenger>> GetPassengersByFlightIdAsync(int flightId);
        Task AddFlightAsync(Flight flight);
        Task SaveChangesAsync();
    }
}
