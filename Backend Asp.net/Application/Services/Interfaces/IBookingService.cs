using Domain.DTOs;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Interfaces
{
    public interface IBookingService
    {
        Task AddBookingAsync(CreateBookingDto createBookingDto);
        Task<List<BookingDto>> GetBookingsByUserId (int userId);
        Task<List<PassengerDto>> GetPassengersByBookingId(int bookingId);
    }
}
