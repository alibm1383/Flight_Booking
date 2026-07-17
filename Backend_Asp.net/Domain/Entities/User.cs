using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    [Index(nameof(PhoneNumber), IsUnique = true)]
    [Index(nameof(Email), IsUnique = true)]
    public class User
    {
        public int Id { get; set; }
        public int RoleId { get; set; }
        [MaxLength(11)]
        public required string PhoneNumber { get; set; }
        [MaxLength(200)]
        public string? Email { get; set; }
        [MaxLength(1000)]
        public required string PasswordHash { get; set; }
        public bool IsActive { get; set; }
        public bool IsEmailVerified { get; set; }
        public bool IsPhoneVerified { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? UpdatedAt { get; set; }
        public DateTime? LastLoginAt { get; set; }
        [MaxLength(1000)]
        public string? ImageUrl { get; set; }

        
        public Role Role { get; set; } = null!;
        public Admin? Admin { get; set; }
        public Customer? Customer { get; set; }
        public Airline? Airline { get; set; }
        public ICollection<Booking> Bookings { get; set; } = [];
    }
}