using Domain.DTOs;
using Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Interfaces
{
    public interface IBookingRepository
    {
        Task AddBookingAsync(Booking booking);
        Task<List<BookingDto>> GetBookingsByUserId(int userId);
        Task<List<Passenger>> GetPassengersByBookingId(int bookingId);
        Task<Booking?> GetBookingByIdAsync(int bookingId);
        Task SaveChangesAsync();
    }
}
