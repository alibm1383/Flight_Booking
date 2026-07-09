using Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.DTOs
{
    public class SearchFlightDto
    {
        public int SourceId { get; set; }
        public int DestinationId { get; set; }
        public int? AirlineId { get; set; }
        public DateOnly DepartureDate { get; set; }
        public TimeOnly? FromTime { get; set; } 
        public TimeOnly? ToTime { get; set; }
        public decimal? MinPrice { get; set; }
        public decimal? MaxPrice { get; set; }
        public FlightSortBy SortBy { get; set; } = FlightSortBy.TimeAsc;
    }
}
