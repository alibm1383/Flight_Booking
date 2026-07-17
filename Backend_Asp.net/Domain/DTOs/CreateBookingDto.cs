using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.DTOs
{
    public class CreateBookingDto
    {
        public int FlightId { get; set; }
        public required List<CreatePassengerDto> Passengers { get; set; }
    }
}
