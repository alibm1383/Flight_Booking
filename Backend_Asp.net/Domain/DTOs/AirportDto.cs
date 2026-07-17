using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.DTOs
{
    public class AirportDto
    {
        public int Id { get; set; }
        public int CityId { get; set; }
        public required string IataCode { get; set; }
        public required string Name { get; set; }
        public string? ImageUrl { get; set; }   
    }
}
