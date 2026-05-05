using Domain.Entities;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Data.Context
{
    public class FlightBookingContext:DbContext
    {
        #region Constructor

        public FlightBookingContext(DbContextOptions<FlightBookingContext> options) : base (options)
        {

        }

        #endregion

        public DbSet<City> Cities  { get; set; }
    }
}
