using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    public class Role
    {
        public int Id { get; set; }
        [MaxLength(200)]
        public required string Name { get; set; }
        public ICollection<User> Users { get; set; } = [];
    }
}
    