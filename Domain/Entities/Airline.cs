using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    public class Airline
    {
        [Key]
        public int UserId { get; set; }
        [MaxLength(200)]
        public required string CompanyName { get; set; }

        public User User { get; set; } = null!;
        public ICollection<Flight> Flights { get; set; } = [];
    }
}
