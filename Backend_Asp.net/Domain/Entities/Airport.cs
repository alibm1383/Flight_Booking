using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    [Index(nameof(IataCode), IsUnique = true)]
    public class Airport
    {
        public int Id { get; set; }
        public int CityId { get; set; }
        [MaxLength(3)]
        public required string IataCode { get; set; }
        [MaxLength(500)]
        public required string Name { get; set; }
        [MaxLength(1000)]
        public string? ImageUrl { get; set; }

        public City City { get; set; } = null!;
        public ICollection<Flight> SourceFlights { get; set; } = [];
        public ICollection<Flight> DestinationFlights { get; set; } = [];

    }
}
