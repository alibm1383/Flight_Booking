using Application.Services.Interfaces;
using AutoMapper;
using Domain.DTOs;
using Domain.Entities;
using Domain.Exceptions;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore.Update;
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
        public async Task AddFlightAsync(CreateFlightDto createFlightDto, int airlineId)
        {
            var flight = _mapper.Map<Flight>(createFlightDto);
            flight.AirlineId = airlineId;
            flight.AvailableSeats = flight.Capacity;
            await _flightRepository.AddFlightAsync(flight);
            await _flightRepository.SaveChangesAsync();
        }

        public async Task<PagedResult<FlightDto>> SearchAsync(SearchFlightDto searchFlightDto)
        {
            var pageResult = await _flightRepository.SearchAsync(searchFlightDto);
            return new PagedResult<FlightDto>()
            {
                Items = _mapper.Map<List<FlightDto>>(pageResult.Items),
                TotalCount = pageResult.TotalCount,
                PageNumber = pageResult.PageNumber,
                PageSize = pageResult.PageSize
            };
        }

        public async Task<FlightDto?> GetFlightByIdAsync(int flightId)
        {
            var flight = await _flightRepository.GetFlightByIdAsync(flightId);
            return _mapper.Map<FlightDto>(flight);
        }

        public async Task<IEnumerable<FlightDto>> GetFlightsByAirlineIdAsync(int airlineId)
        {
            var flights = await _flightRepository.GetFlightsByAirlineIdAsync(airlineId);
            return _mapper.Map<IEnumerable<FlightDto>>(flights);
        }

        public async Task<IEnumerable<PassengerDto>> GetPassengersByFlightIdAsync(int flightId, int airlineId)
        {
            var flight = await _flightRepository.GetFlightByIdAsync(flightId);
            if (flight == null)
            {
                throw new NotFoundException("Flight not found.");
            }
            if (flight.AirlineId != airlineId)
            {
                throw new ForbiddenException("Access denied.");
            }
            var passengers = await _flightRepository.GetPassengersByFlightIdAsync(flightId);
            return _mapper.Map<IEnumerable<PassengerDto>>(passengers);
        }
    }
}
