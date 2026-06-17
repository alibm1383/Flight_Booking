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
    [Index(nameof(PnrCode), IsUnique = true)]
    public class Booking
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public int FlightId { get; set; }
        public int SeatCount { 
            get 
            {
                return Passengers.Count;
            } }
        public DateTime BookingDate { get; set; }
        [MaxLength(50)]
        public required string PnrCode { get; set; }
        [Precision(18, 3)]
        public decimal TotalAmount { get; set; }

        public User User { get; set; } = null!;
        public Flight Flight { get; set; } = null!;
        public ICollection<Passenger> Passengers { get; set; } = [];

    }
}
