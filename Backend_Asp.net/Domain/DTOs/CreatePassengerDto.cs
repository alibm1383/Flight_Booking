using Domain.Entities;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.DTOs
{
    public class CreatePassengerDto
    {
        [MaxLength(200)]
        public required string FirstName { get; set; }
        [MaxLength(200)]
        public required string LastName { get; set; }
        [MaxLength(10)]
        public required string NationalCode { get; set; }
        public DateOnly BirthDate { get; set; }
        public Gender Gender { get; set; }
    }
}
