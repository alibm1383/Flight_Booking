using Domain.DTOs;
using Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Interfaces
{
    public interface IAirportService
    {
        Task<IEnumerable<AirportDto>> GetAllAirportsAsync();
        Task<AirportDto?> GetAirportByIdAsync(int airportId);   
        Task AddAirportAsync(CreateAirportDto createAirportDto);
    }
}
