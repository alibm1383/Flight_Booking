using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.DTOs
{
    public class CreateAirportDto
    {
        public int CityId { get; set; }
        [MaxLength(3)]
        public required string IataCode { get; set; }
        [MaxLength(500)]
        public required string Name { get; set; }
        public IFormFile? Image { get; set; }
    }
}
