using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Metadata.Ecma335;
using System.Text;
using System.Threading.Tasks;

namespace Domain.DTOs
{
    public class BookingDto
    {
        public int Id { get; set; }
        public string SourceCity { get; set; }
        public string DestinationCity { get; set; }
        public string AirlineName { get; set; }
        public DateTime DepartureTime { get; set; }
        public string FlightNumber { get; set; }
        public required string PnrCode { get; set; }
        public decimal TotalAmount { get; set; }
    }
}
