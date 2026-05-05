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
    [Index(nameof(IataCode), IsUnique = true)]
    public class Airport
    {
        [Key]
        public int Id { get; set; }
        public int CityId { get; set; }
        [MaxLength(3)]
        public required string IataCode { get; set; }
        [MaxLength(500)]
        public string? ImageUrl { get; set; }

        [ForeignKey(nameof(CityId))]
        public City City { get; set; } = null!;
    }
}
