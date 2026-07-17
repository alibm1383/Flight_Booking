using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Reflection.Metadata.Ecma335;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    [Index(nameof(FlightNumber), IsUnique = true)]
    public class Flight
    {
        public int Id { get; set; }
        public int AirlineId { get; set; }
        public int SourceId { get; set; }
        public int DestinationId { get; set; }
        [MaxLength(50)]
        public required string FlightNumber { get; set; }
        public DateTime DepartureTime { get; set; }
        public DateTime ArrivalTime { get; set; }
        public int Capacity { get; set; }
        public int AvailableSeats { get; set; }
        [Precision(18, 3)]
        public decimal Price { get; set; }
        [MaxLength(1000)]
        public string? Description { get; set; }

        public Airline Airline { get; set; } = null!;
        public Airport Source { get; set; } = null!;
        public Airport Destination { get; set; } = null!;
        public ICollection<Booking> Bookings { get; set; } = [];

    }
}
