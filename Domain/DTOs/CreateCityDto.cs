using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;

namespace Domain.DTOs
{
    public class CreateCityDto
    {
        [Required]
        [MaxLength(100)]
        public required string Name { get; set; }
        public IFormFile? Image { get; set; }
    }
}
