using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    public class City
    {
        #region Properties
        [Key]
        public int Id { get; set; }
        [MaxLength(100)]
        public required string Name { get; set; }
        [MaxLength(500)]
        public string? ImageUrl { get; set; }
        public ICollection<Airport> Airports { get; set; } = new List<Airport>();   
        #endregion
    }
}

