using Domain.Entities;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.DTOs
{
    public class CreateFlightDto
    {
        public int SourceId { get; set; }
        public int DestinationId { get; set; }
        [MaxLength(50)]
        public required string FlightNumber { get; set; }
        public DateTime DepartureTime { get; set; }
        public DateTime ArrivalTime { get; set; }
        public int Capacity { get; set; }
        [Precision(18, 3)]
        public decimal Price { get; set; }
        [MaxLength(1000)]
        public string? Description { get; set; }
    }
}
