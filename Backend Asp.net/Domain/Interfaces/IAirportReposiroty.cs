using Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Interfaces
{
    public interface IAirportReposiroty
    {
        Task<IEnumerable<Airport>> GetAllAirportsAsync();
        Task<Airport?> GetAirportByIdAsync(int airportId);
        Task AddAirportAsync(Airport airport);
        Task SaveChangesAsync();
    }
}
