using Application.Services.Interfaces;
using AutoMapper;
using Domain.DTOs;
using Domain.Entities;
using Domain.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Implementations
{
    public class FlightService : IFlightService
    {
        private readonly IFlightRepository _flightRepository;
        private readonly IMapper _mapper;

        public FlightService(IFlightRepository flightRepository, IMapper mapper)
        {
            _flightRepository = flightRepository;
            _mapper = mapper;
        }
        public async Task AddFlightAsync(CreateFlightDto createFlightDto)
        {
            var flight = _mapper.Map<Flight>(createFlightDto);
            flight.AvailableSeats = flight.Capacity;
            await _flightRepository.AddFlightAsync(flight);
            await _flightRepository.SaveChangesAsync();
        }

        public async Task<IEnumerable<FlightDto>> GetAllFlightsAsync()
        {
            var flights = await _flightRepository.GetAllFlightsAsync();
            return _mapper.Map<IEnumerable<FlightDto>>(flights);
        }

        public async Task<FlightDto?> GetFlightByIdAsync(int flightId)
        {
            var flight = await _flightRepository.GetFlightByIdAsync(flightId);
            return _mapper.Map<FlightDto>(flight);
        }
    }
}
