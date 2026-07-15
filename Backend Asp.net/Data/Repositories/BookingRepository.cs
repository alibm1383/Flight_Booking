using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Data.Context;
using Domain.DTOs;
using Domain.Entities;
using Domain.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Data.Repositories
{
    public class BookingRepository : IBookingRepository
    {
        private readonly FlightBookingContext _context;

        public BookingRepository(FlightBookingContext context)
        {
            _context = context;
        }

        public async Task AddBookingAsync(Booking booking)
        {
            await _context.Bookings.AddAsync(booking);
        }

        public async Task<Booking?> GetBookingByIdAsync(int bookingId)
        {
            return await _context.Bookings.FirstOrDefaultAsync(b => b.Id == bookingId);
        }

        public async Task<List<BookingDto>> GetBookingsByUserId(int userId)
        {
            return await _context.Bookings
                .Where(b => b.UserId == userId)
                .Select(b => new BookingDto
                {
                    Id = b.Id,
                    TotalAmount = b.TotalAmount,
                    PnrCode = b.PnrCode,
                    FlightNumber = b.Flight.FlightNumber,
                    DepartureTime = b.Flight.DepartureTime,
                    AirlineName = b.Flight.Airline.CompanyName,
                    SourceCity = b.Flight.Source.City.Name,
                    DestinationCity = b.Flight.Destination.City.Name
                }).ToListAsync();
        }

        public async Task<List<Passenger>> GetPassengersByBookingId(int bookingId)
        {
            return await _context.Passengers.Where(p => p.BookingId == bookingId).ToListAsync();
        }

        public async Task SaveChangesAsync()
        {
           await _context.SaveChangesAsync();
        }
    }
}
