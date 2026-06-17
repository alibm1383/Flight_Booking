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

        #region FluentAPI
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Admin>()
            .HasOne(a => a.User)
            .WithOne(u => u.Admin)
            .HasForeignKey<Admin>(a => a.UserId);

            modelBuilder.Entity<Customer>()
                .HasOne(c => c.User)
                .WithOne(u => u.Customer)
                .HasForeignKey<Customer>(c => c.UserId);

            modelBuilder.Entity<Airline>()
                .HasOne(a => a.User)
                .WithOne(u => u.Airline)
                .HasForeignKey<Airline>(a => a.UserId);

            modelBuilder.Entity<Flight>()
            .HasOne(f => f.Source)
            .WithMany(a => a.SourceFlights)
            .HasForeignKey(f => f.SourceId)
            .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Flight>()
                .HasOne(f => f.Destination)
                .WithMany(a => a.DestinationFlights)
                .HasForeignKey(f => f.DestinationId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Role>().HasData(
            new Role
            {
                Id = 1,
                Name = "Admin"
            },
            new Role
            {
                Id = 2,
                Name = "Airline"
            },
            new Role
            {
                Id = 3,
                Name = "Customer"
            });

        }
        #endregion

        public DbSet<City> Cities  { get; set; }
        public DbSet<User> Users { get; set; }
        public DbSet<Role> Roles { get; set; }
        public DbSet<Admin> Admins { get; set; }
        public DbSet<Customer> Customers { get; set; }
        public DbSet<Airline> Airlines { get; set; }
        public DbSet<Airport> Airports { get; set; }
        public DbSet<Flight> Flights { get; set; }
        public DbSet<Booking> Bookings { get; set; }
        public DbSet<Passenger> Passengers { get; set; }
    }
}
