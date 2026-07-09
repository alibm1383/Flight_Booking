using Domain.Entities;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.DTOs
{
    public class PassengerDto
    {
        public int Id { get; set; }
        public required string FirstName { get; set; }
        public required string LastName { get; set; }   
        public required string NationalCode { get; set; }
        public DateOnly BirthDate { get; set; }
        public Gender Gender { get; set; }
    }
}
