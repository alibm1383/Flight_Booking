using Domain.DTOs;
using Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Interfaces
{
    public interface IFlightService
    {
        Task<IEnumerable<FlightDto>> SearchAsync(SearchFlightDto searchFlightDto);
        Task<IEnumerable<FlightDto>> GetFlightsByAirlineIdAsync(int airlineId);
        Task<IEnumerable<PassengerDto>> GetPassengersByFlightIdAsync(int flightId);
        Task<FlightDto?> GetFlightByIdAsync(int flightId);
        Task AddFlightAsync(CreateFlightDto createFlightDto);
    }
}
