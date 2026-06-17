using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    public class Customer
    {
        [Key]
        public int UserId { get; set; }
        [MaxLength(200)]
        public required string FirstName { get; set; }
        [MaxLength(200)]
        public required string LastName { get; set; }
        public DateOnly? BirthDate { get; set; }
        public Gender Gender { get; set; }

        public User User { get; set; } = null!;
    }
}
